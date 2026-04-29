# Honest DiD bounds (Rambachan & Roth 2023) for the v2-conservative
# Callaway-Sant'Anna event study.
#
# Implements the smoothness restriction: post-treatment differential trend
# slope cannot deviate from the pre-treatment trend slope by more than M
# per period. M = 0 corresponds to "trends extrapolate exactly," M >> 0
# allows arbitrary deviations.
#
# Outputs:
#   analysis/did_honest_bounds_v2_conservative.csv   numeric bounds
#   analysis/did_honest_bounds_v2_conservative.png   sensitivity plot

repos <- "https://cloud.r-project.org"
needed <- c("did", "data.table", "HonestDiD", "ggplot2")
for (pkg in needed) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
        cat(sprintf("Installing %s ...\n", pkg))
        install.packages(pkg, repos = repos, quiet = TRUE,
                         lib = Sys.getenv("R_LIBS_USER"))
    }
}

suppressPackageStartupMessages({
    library(did)
    library(data.table)
    library(HonestDiD)
    library(ggplot2)
})

cat(sprintf("did %s, HonestDiD %s\n",
            packageVersion("did"), packageVersion("HonestDiD")))

# --- Load panel and re-fit CS  ---------------------------------------------

panel_path <- "analysis/did_panel_v2_conservative.csv"
if (!file.exists(panel_path)) {
    args <- commandArgs(trailingOnly = FALSE)
    file_arg <- sub("--file=", "", args[grep("--file=", args)])
    if (length(file_arg) > 0) {
        script_dir <- dirname(normalizePath(file_arg))
        panel_path <- file.path(script_dir, "did_panel_v2_conservative.csv")
    }
}
stopifnot(file.exists(panel_path))

dt <- fread(panel_path)
setDT(dt)
dt[, state_id := as.integer(factor(state))]
dt[, cohort_num := as.numeric(cohort)]

set.seed(42)
fit <- att_gt(
    yname = "rate_per_1000_estabs",
    tname = "year",
    idname = "state_id",
    gname = "cohort_num",
    data = dt,
    control_group = "notyettreated",
    bstrap = TRUE,
    biters = 999,
    cband = TRUE,
    panel = TRUE,
    allow_unbalanced_panel = TRUE,
    est_method = "reg",
    faster_mode = FALSE
)

# Need the *event-study aggregation* (dynamic) for HonestDiD. We pass the
# full event-time vector including pre and post periods. The HonestDiD
# package needs:
#   betahat: event-study coefficients (excluding the omitted reference period -1)
#   sigma:   their variance-covariance matrix
#   numPrePeriods, numPostPeriods

es <- aggte(fit, type = "dynamic", min_e = -6, max_e = 6, na.rm = TRUE,
            bstrap = TRUE, biters = 999, cband = TRUE)

# HonestDiD expects:
#   betahat: vector excluding the reference period (event-time -1)
#   sigma: (length(betahat))^2 covariance matrix excluding the reference row/col
#   numPrePeriods = number of event times in betahat with t < 0
#   numPostPeriods = number of event times in betahat with t >= 0

event_times_full <- es$egt
betahat_full <- es$att.egt

# Build covariance matrix. The CS package returns:
#   es$se.egt   - bootstrap-based SEs (what its CI uses)
#   es$inf.function$dynamic.inf.func.e - influence-function matrix (n_cluster x K)
# These two don't agree exactly because aggte uses bootstrap critical values,
# not analytical asymptotic SEs. For HonestDiD we need a vcov on the scale
# of the SEs, so we take the correlation structure from the influence function
# and rescale to match the bootstrap SEs on the diagonal.
inf_e <- es$inf.function$dynamic.inf.func.e
if (is.null(inf_e) && !is.null(es$inf.function$dynamic.inf.func)) {
    inf_e <- es$inf.function$dynamic.inf.func
}
if (!is.null(inf_e)) {
    n <- nrow(inf_e)
    # Analytical variance estimator: (1/n^2) * IF' * IF
    V_analytical <- (t(inf_e) %*% inf_e) / (n * n)
    # Rescale: keep correlation structure, swap diagonal for bootstrap SEs^2
    se_diag <- es$se.egt
    se_analytical <- sqrt(diag(V_analytical))
    # Avoid division by zero in degenerate columns
    safe_scale <- ifelse(se_analytical > 1e-9, se_diag / se_analytical, 1)
    D <- diag(safe_scale)
    Vhat_full <- D %*% V_analytical %*% D
    rownames(Vhat_full) <- as.character(event_times_full)
    colnames(Vhat_full) <- as.character(event_times_full)
    cat(sprintf("Using IF-correlation rescaled to match bootstrap SEs.\n"))
    cat(sprintf("  bootstrap se.egt:  %s\n",
                paste(round(se_diag, 3), collapse=" ")))
    cat(sprintf("  analytical sqrt(V): %s\n",
                paste(round(se_analytical, 3), collapse=" ")))
} else {
    cat("[WARN] influence function not available — using diagonal of bootstrap SEs.\n")
    Vhat_full <- diag(es$se.egt^2)
    rownames(Vhat_full) <- as.character(event_times_full)
    colnames(Vhat_full) <- as.character(event_times_full)
}

# Drop the reference period (event time -1)
keep <- which(event_times_full != -1)
event_times <- event_times_full[keep]
betahat <- betahat_full[keep]
sigma <- Vhat_full[keep, keep]

numPrePeriods <- sum(event_times < 0)
numPostPeriods <- sum(event_times >= 0)

cat("\nEvent-time vector (after dropping reference -1):\n")
print(event_times)
cat(sprintf("betahat length: %d\n", length(betahat)))
cat(sprintf("sigma dim: %d x %d\n", nrow(sigma), ncol(sigma)))
cat(sprintf("numPrePeriods = %d (event times -%d through -2)\n",
            numPrePeriods, numPrePeriods + 1))
cat(sprintf("numPostPeriods = %d (event times 0 through %d)\n",
            numPostPeriods, numPostPeriods - 1))

# --- Run honest sensitivity for several M values ---------------------------

# HonestDiD's smoothness restriction: |delta_t - delta_{t-1}| <= M for the
# linear pre-trend extrapolation. M=0 means linear extrapolation; larger M
# allows greater deviations. The package documentation uses Mbar in some
# versions and M in others.
M_values <- c(0, 0.5, 1, 2)

# Sensitivity for the OVERALL ATT (average of post-treatment event-time effects)
# is the most policy-relevant single number. Also produce per-event-time bounds.
sens_overall <- list()
for (m in M_values) {
    res <- createSensitivityResults(
        betahat = betahat,
        sigma = sigma,
        numPrePeriods = numPrePeriods,
        numPostPeriods = numPostPeriods,
        method = "C-LF",   # least favorable (default for smoothness)
        Mvec = m,
        l_vec = rep(1 / numPostPeriods, numPostPeriods)  # equal-weight average
    )
    sens_overall[[as.character(m)]] <- res
    cat(sprintf("\nM = %.2f:\n", m))
    print(res)
}

# Also compute the original (unrestricted) CI for comparison
orig_ci <- constructOriginalCS(
    betahat = betahat,
    sigma = sigma,
    numPrePeriods = numPrePeriods,
    numPostPeriods = numPostPeriods,
    l_vec = rep(1 / numPostPeriods, numPostPeriods)
)
cat(sprintf("\nOriginal CS confidence interval (no honest restriction):\n"))
print(orig_ci)

# --- Also run relative-magnitudes restriction for comparison ---------------
# Mbar=1 corresponds to "post-treatment violations no larger than the
# largest pre-treatment violation," the most-cited Rambachan-Roth bound.

Mbar_values <- c(0.5, 1, 2)
sens_rm <- list()
for (mb in Mbar_values) {
    res <- createSensitivityResults_relativeMagnitudes(
        betahat = betahat,
        sigma = sigma,
        numPrePeriods = numPrePeriods,
        numPostPeriods = numPostPeriods,
        Mbarvec = mb,
        l_vec = rep(1 / numPostPeriods, numPostPeriods)
    )
    sens_rm[[as.character(mb)]] <- res
    cat(sprintf("\nMbar (rel. magnitudes) = %.2f:\n", mb))
    print(res)
}

# --- Build a tidy results table --------------------------------------------

results_df <- data.frame(
    restriction = c("Original (CS unrestricted)",
                     rep("Smoothness (DeltaSD)", length(M_values)),
                     rep("Relative magnitudes (DeltaRM)", length(Mbar_values))),
    parameter = c("",
                   sprintf("M = %.2f", M_values),
                   sprintf("Mbar = %.2f", Mbar_values)),
    lb = c(orig_ci$lb,
            sapply(sens_overall, function(x) x$lb),
            sapply(sens_rm, function(x) x$lb)),
    ub = c(orig_ci$ub,
            sapply(sens_overall, function(x) x$ub),
            sapply(sens_rm, function(x) x$ub)),
    method = c(orig_ci$method,
                sapply(sens_overall, function(x) x$method),
                sapply(sens_rm, function(x) x$method))
)
results_df$width <- results_df$ub - results_df$lb

cat("\n--- Sensitivity bounds table ---\n")
print(results_df)

write.csv(results_df,
          "analysis/did_honest_bounds_v2_conservative.csv",
          row.names = FALSE)

# --- Sensitivity plot ------------------------------------------------------

# Combine deltaSD and deltaRM rows for plotting
sd_rows <- do.call(rbind, lapply(seq_along(M_values), function(i) {
    data.frame(label = sprintf("M=%.2g", M_values[i]),
               restriction = "Smoothness",
               lb = sens_overall[[i]]$lb,
               ub = sens_overall[[i]]$ub,
               x_order = i + 1)
}))
rm_rows <- do.call(rbind, lapply(seq_along(Mbar_values), function(i) {
    data.frame(label = sprintf("Mbar=%.2g", Mbar_values[i]),
               restriction = "Relative magnitudes",
               lb = sens_rm[[i]]$lb,
               ub = sens_rm[[i]]$ub,
               x_order = length(M_values) + 1 + i)
}))
orig_row <- data.frame(label = "Original CS",
                        restriction = "Original",
                        lb = orig_ci$lb,
                        ub = orig_ci$ub,
                        x_order = 1)
plot_df <- rbind(orig_row, sd_rows, rm_rows)
plot_df$label <- factor(plot_df$label, levels = plot_df$label[order(plot_df$x_order)])

p <- ggplot(plot_df, aes(x = label,
                          y = (lb + ub) / 2,
                          ymin = lb, ymax = ub,
                          colour = restriction)) +
    geom_pointrange(size = 0.6) +
    geom_hline(yintercept = 0, linetype = "dashed", colour = "grey40") +
    labs(
        title = "Honest DiD sensitivity bounds — average post-treatment ATT (v2-conservative)",
        subtitle = "Larger M / Mbar = weaker assumption about pre-trends, wider bounds",
        x = "Restriction",
        y = "ATT (new 401(k) plans per 1,000 establishments)",
        caption = "Original CS = unrestricted bootstrap CI. DeltaSD = smoothness; DeltaRM = relative magnitudes (Rambachan & Roth 2023).",
        colour = NULL
    ) +
    theme_minimal(base_size = 11) +
    theme(legend.position = "bottom",
          axis.text.x = element_text(angle = 30, hjust = 1))

ggsave("analysis/did_honest_bounds_v2_conservative.png",
       plot = p, width = 9, height = 5.5, dpi = 120)

cat("\nWrote:\n  analysis/did_honest_bounds_v2_conservative.csv\n  analysis/did_honest_bounds_v2_conservative.png\n")
