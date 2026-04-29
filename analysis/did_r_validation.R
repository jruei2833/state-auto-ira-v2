# R cross-validation of the Python `differences` Callaway-Sant'Anna estimate.
#
# Runs att_gt() on the v2-conservative panel, aggregates to a simple ATT,
# and writes the headline + event-study + cohort tables to CSV for direct
# comparison with the Python output.
#
# Usage:
#   Rscript analysis/did_r_validation.R

# --- bootstrap CRAN if needed -----------------------------------------------

repos <- "https://cloud.r-project.org"
needed <- c("did", "data.table")
for (pkg in needed) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
        cat(sprintf("Installing %s ...\n", pkg))
        install.packages(pkg, repos = repos, quiet = TRUE)
    }
}

suppressPackageStartupMessages({
    library(did)
    library(data.table)
})

cat(sprintf("did package version: %s\n", as.character(packageVersion("did"))))

# --- load panel -------------------------------------------------------------

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
cat(sprintf("Loading panel: %s\n", panel_path))

dt <- fread(panel_path)

# --- prepare for did::att_gt() ---------------------------------------------
# `did` requires a numeric entity id; cohort=0 means never-treated;
# control_group "notyettreated" matches the Python "not_yet_treated" arm.

setDT(dt)
dt[, state_id := as.integer(factor(state))]
# `did` rewrites never-treated cohort = 0 to Inf internally during
# preprocessing; if we pass an integer column, that coercion produces NA
# and att_gt() errors out with a "singular matrix" message. Pass numeric.
dt[, cohort_num := as.numeric(cohort)]

cat("\nCohort distribution:\n")
print(dt[, .(states = uniqueN(state)), by = cohort_num])

# --- fit ATT(g,t) -----------------------------------------------------------

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

cat("\n--- raw group-time ATT(g,t) ---\n")
print(summary(fit))

# --- aggregate to overall ATT ----------------------------------------------

agg_simple <- aggte(fit, type = "simple", bstrap = TRUE, biters = 999, cband = TRUE)
cat("\n--- simple aggregation (overall ATT) ---\n")
print(summary(agg_simple))

agg_event <- aggte(fit, type = "dynamic", bstrap = TRUE, biters = 999, cband = TRUE,
                   min_e = -6, max_e = 6)
cat("\n--- dynamic / event-time aggregation ---\n")
print(summary(agg_event))

agg_cohort <- aggte(fit, type = "group", bstrap = TRUE, biters = 999, cband = TRUE)
cat("\n--- cohort aggregation ---\n")
print(summary(agg_cohort))

# --- write CSVs for cross-language comparison -----------------------------

out_dir <- dirname(panel_path)

simple_df <- data.frame(
    type      = "simple",
    estimate  = agg_simple$overall.att,
    std_error = agg_simple$overall.se,
    ci_lo     = agg_simple$overall.att - 1.96 * agg_simple$overall.se,
    ci_hi     = agg_simple$overall.att + 1.96 * agg_simple$overall.se
)
write.csv(simple_df, file.path(out_dir, "did_r_simple_v2_conservative.csv"),
          row.names = FALSE)

event_df <- data.frame(
    event_time = agg_event$egt,
    estimate   = agg_event$att.egt,
    std_error  = agg_event$se.egt,
    ci_lo      = agg_event$att.egt - agg_event$crit.val.egt * agg_event$se.egt,
    ci_hi      = agg_event$att.egt + agg_event$crit.val.egt * agg_event$se.egt
)
write.csv(event_df, file.path(out_dir, "did_r_event_v2_conservative.csv"),
          row.names = FALSE)

cohort_df <- data.frame(
    cohort    = agg_cohort$egt,
    estimate  = agg_cohort$att.egt,
    std_error = agg_cohort$se.egt,
    ci_lo     = agg_cohort$att.egt - agg_cohort$crit.val.egt * agg_cohort$se.egt,
    ci_hi     = agg_cohort$att.egt + agg_cohort$crit.val.egt * agg_cohort$se.egt
)
write.csv(cohort_df, file.path(out_dir, "did_r_cohort_v2_conservative.csv"),
          row.names = FALSE)

cat("\n========================================\n")
cat(sprintf("R simple ATT: %.4f (SE %.4f)\n",
            agg_simple$overall.att, agg_simple$overall.se))
cat("Outputs written:\n")
cat(sprintf("  %s\n  %s\n  %s\n",
            file.path(out_dir, "did_r_simple_v2_conservative.csv"),
            file.path(out_dir, "did_r_event_v2_conservative.csv"),
            file.path(out_dir, "did_r_cohort_v2_conservative.csv")))
cat("========================================\n")
