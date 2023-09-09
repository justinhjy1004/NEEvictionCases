library(tidyverse)
library(knitr)
library(lubridate)
library(stargazer)

df <- read_csv("../Data/AllEvictionCases.csv")

df |>
  mutate(
    FILING_DATE = as.Date(FILING_DATE, format = "%m/%d/%Y"), 
    CLOSING_DATE = as.Date(CLOSING_DATE, format = "%m/%d/%Y"),
    DAYS = as.numeric(difftime(ymd(CLOSING_DATE), 
                        ymd(FILING_DATE), units = "days"))
  ) -> df

df$ATTEMPT <- grepl("attempt", df$ACTIONS, ignore.case = TRUE)
df$DEFAULT <- grepl("default", df$ACTIONS, ignore.case = TRUE)

df$ATTEMPT <- ifelse(df$ATTEMPT, "Multiple Attempts", "Single Attempt")
df$DEFAULT <- ifelse(df$DEFAULT, "Default Judgment", "Not Default")
df$HAS_HEARINGS <- ifelse(df$NUM_HEARINGS != 0, "Had Hearing(s)", "No Hearing")

table(df$COURT, df$HAS_HEARINGS) -> freq_hearings_court
kable(freq_hearings_court, format = "latex", booktabs = TRUE)

round(prop.table(freq_hearings_court, margin = 1), 3) -> dist_hearings_court
kable(dist_hearings_court, format = "latex", booktabs = TRUE)

lancaster <- df[df$COURT == "Lancaster",]
table(lancaster$HAS_HEARINGS, lancaster$ATTEMPT) |>
  prop.table(margin=1) |>
  kable( format = "latex", booktabs = TRUE )

table(lancaster$HAS_HEARINGS, lancaster$DEFAULT) |>
  prop.table(margin=1) |>
  kable( format = "latex", booktabs = TRUE )

douglas <- df[df$COURT == "Douglas",]

table(douglas$HAS_HEARINGS, douglas$ATTEMPT) |>
  prop.table(margin=1) |>
  kable( format = "latex", booktabs = TRUE )

table(douglas$HAS_HEARINGS, douglas$DEFAULT) |>
  prop.table(margin=1) |>
  kable( format = "latex", booktabs = TRUE )

df |>
  select(-CASE_SUMMARY, -JUDGEMENT_INFO, -ACTIONS, -PARTIES)  |>
  filter( YEAR != 2023) |>
  mutate( 
    YEAR = as.factor(YEAR),
    DEF_HAS_ATTORNEY = ifelse(is.na(DEFENDANT_ATTORNEY), FALSE, TRUE),
    DEF_HAS_REP = DEF_HAS_ATTORNEY | HAS_LIMITED_REPRESENTATION
  )  -> df

reg1 <- lm(DEF_HAS_REP ~ HAS_HEARINGS, df)
summary(reg1)

reg2 <- lm(JUDGMENT ~ HAS_HEARINGS, df)
summary(reg2)

reg3 <- lm(DAYS ~ HAS_HEARINGS, df)
summary(reg3)

stargazer(reg1, reg2, reg3)
