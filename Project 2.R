# =============================================================================
# Project 2: Predictive Valuation & Macro Risk Assessment of UK CRE
# Step 2: Multiple Linear Regression Analysis in R
# =============================================================================

# 1. Install & Load Packages 

install.packages(c("readxl", "dplyr", "ggplot2", "corrplot", "lmtest",
                   "sandwich", "stargazer", "car"))

library(readxl)
library(dplyr)
library(ggplot2)
library(corrplot)
library(lmtest)      # Breusch-Pagan test for heteroskedasticity
library(sandwich)    # Robust standard errors
library(stargazer)   # Clean regression output table
library(car)         # VIF (multicollinearity check)


# 2. Load Data

file_path <- "/Users/henrystead/Desktop/Project 2/CRE+Macro.xlsx"

df <- read_excel(file_path, sheet = "Sheet1")

# Convert all yield/rate columns from decimal to percentage for readability
df <- df %>%
  mutate(
    BoE_Rate       = `BoE Base Rate (%)` * 100,
    CPI            = `CPI Inflation (%)`  * 100,
    GDP_Growth     = `GDP Growth (%)`     * 100,
    London_Yield   = `London Office Yield (%)` * 100,
    Regional_Yield = `Regional Office Yield (%)` * 100
  )

# Decode the Excel date serial number to a proper Date
df <- df %>%
  mutate(Date = as.Date(Date, origin = "1899-12-30"))

# Add a numeric time index (useful for trend checks)
df <- df %>%
  mutate(Time_Index = row_number())

cat("Data loaded successfully. Rows:", nrow(df), "\n\n")
print(df %>% select(Date, Period, BoE_Rate, CPI, GDP_Growth, London_Yield, Regional_Yield))


# 3. Exploratory Data Analysis (EDA)

cat("\n--- Summary Statistics ---\n")
print(summary(df %>% select(BoE_Rate, CPI, GDP_Growth, London_Yield, Regional_Yield)))

# Correlation matrix
cor_matrix <- cor(df %>% select(BoE_Rate, CPI, GDP_Growth, London_Yield, Regional_Yield),
                  use = "complete.obs")
cat("\n--- Correlation Matrix ---\n")
print(round(cor_matrix, 3))

# Plot correlation matrix
corrplot(cor_matrix,
         method      = "color",
         type        = "upper",
         tl.col      = "black",
         tl.srt      = 45,
         addCoef.col = "black",
         number.cex  = 0.8,
         title       = "Correlation Matrix: CRE Yields & Macro Indicators",
         mar         = c(0, 0, 2, 0))


# 4. Multiple Linear Regression: London Office Yield

cat("\n\n=== MODEL 1: London Office Yield ===\n")

model_london <- lm(London_Yield ~ BoE_Rate + CPI + GDP_Growth, data = df)

summary(model_london)

# Variance Inflation Factor — check for multicollinearity
cat("\n--- VIF (London Model) ---\n")
print(vif(model_london))

# Breusch-Pagan test — check for heteroskedasticity
cat("\n--- Breusch-Pagan Test (London Model) ---\n")
print(bptest(model_london))

# Robust standard errors (HAC — appropriate for time series)
cat("\n--- Robust Standard Errors (London Model) ---\n")
coeftest(model_london, vcov = vcovHAC(model_london))


# 5. Multiple Linear Regression: Regional Office Yield 

cat("\n\n=== MODEL 2: Regional Office Yield ===\n")

model_regional <- lm(Regional_Yield ~ BoE_Rate + CPI + GDP_Growth, data = df)

summary(model_regional)

cat("\n--- VIF (Regional Model) ---\n")
print(vif(model_regional))

cat("\n--- Breusch-Pagan Test (Regional Model) ---\n")
print(bptest(model_regional))

cat("\n--- Robust Standard Errors (Regional Model) ---\n")
coeftest(model_regional, vcov = vcovHAC(model_regional))


# 5b. Extract HAC standard errors for use in stargazer

hac_se_london   <- sqrt(diag(vcovHAC(model_london)))
hac_se_regional <- sqrt(diag(vcovHAC(model_regional)))


# 6. Side-by-Side Regression Table (Stargazer) — now using HAC SEs

stargazer(model_london, model_regional,
          type             = "text",
          title            = "Regression Results: UK CRE Yields vs Macro Indicators",
          dep.var.labels   = c("London Office Yield (%)", "Regional Office Yield (%)"),
          covariate.labels = c("BoE Base Rate (%)", "CPI Inflation (%)", "GDP Growth (%)"),
          se               = list(hac_se_london, hac_se_regional),
          omit.stat        = c("f", "ser"),
          notes            = "HAC (Andrews quadratic-spectral) robust standard errors in parentheses",
          notes.append     = TRUE,
          digits           = 3)


# 7. Diagnostic Plots — each plot shown individually in the Plots pane

# Reset plotting layout to a single panel (undo any previous par(mfrow) setting)
par(mfrow = c(1, 1))

# London model — Residuals vs Fitted, Q-Q, Scale-Location, Residuals vs Leverage
for (i in c(1, 2, 3, 5)) {
  plot(model_london, which = i)
}

# Regional model — same four plots
for (i in c(1, 2, 3, 5)) {
  plot(model_regional, which = i)
}


# 8. Actual vs Fitted Plots 

par(mfrow = c(1, 1))

# London
df$London_Fitted <- fitted(model_london)
print(
  ggplot(df, aes(x = Date)) +
    geom_line(aes(y = London_Yield,  colour = "Actual"), linewidth = 1) +
    geom_line(aes(y = London_Fitted, colour = "Fitted"), linewidth = 1, linetype = "dashed") +
    labs(title  = "London Office Yield: Actual vs Fitted",
         x      = "Date",
         y      = "Yield (%)",
         colour = "") +
    theme_minimal()
)

# Regional
df$Regional_Fitted <- fitted(model_regional)
print(
  ggplot(df, aes(x = Date)) +
    geom_line(aes(y = Regional_Yield,  colour = "Actual"), linewidth = 1) +
    geom_line(aes(y = Regional_Fitted, colour = "Fitted"), linewidth = 1, linetype = "dashed") +
    labs(title  = "Regional Office Yield: Actual vs Fitted",
         x      = "Date",
         y      = "Yield (%)",
         colour = "") +
    theme_minimal()
)