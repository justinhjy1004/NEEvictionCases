library(tidyverse)
library(predictrace)

df <- read_csv("../Data/NamedDefendants.csv")

#=============================================================
# Split names based on First and Last
# Predict Gender and Race from Name
#=============================================================
df <- df |>
  select(CASE_ID, NAMED_DEFENDANTS) |>
  extract(
    NAMED_DEFENDANTS, c("D_FIRST", "D_LAST"), "([^ ]+) (.*)", remove = FALSE
    ) |>
  mutate(
    PRED_RACE_FIRST = predict_race(D_FIRST, surname = FALSE, probability = FALSE)[[3]],
    PRED_RACE_LAST = predict_race(D_LAST, surname = TRUE, probability = FALSE)[[3]],
    PRED_GENDER = predict_gender(D_FIRST, probability = FALSE)[[3]]
  )

write.csv(df, file = "../Data/NamedDefendants.csv", row.names = FALSE)
