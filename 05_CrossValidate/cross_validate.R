library(tidyverse)
library(readxl)
library(lubridate)
library(stringr)

# Get Relevant Fields
sullivan <- read_xlsx("../Data/Sullivan.xlsx", sheet = 2)

# Get Relevant Columns
sullivan |>
  mutate(
    case_num = ifelse(grepl("-", case_num), 
                      str_split(case_num, "-", simplify = TRUE)[,2], 
                      case_num),
    case_num = as.numeric(case_num)
  ) |>
  filter(!is.na(case_num)) |>
  distinct() -> sullivan


# Get CASE_ID for joins
sullivan |>
  mutate(
    case_id = paste0("CI 02 ", year %% 100, "-", case_num) 
    ) -> sullivan

# Get repeats
sullivan |>
  group_by(case_id) |>
  summarize( count = n() ) |>
  filter( count > 1 ) -> repeats

# Remove repeats
sullivan <- sullivan[!(sullivan$case_id %in% repeats$case_id),]

# Recode Sullivan's data
sullivan |> 
  mutate(
    writ = ifelse(writ_outcome != "N/A", TRUE, FALSE),
    change_locks = ifelse(writ_outcome == "Executed", TRUE, FALSE)
  ) -> sullivan

data <- read_csv("../Data/AllEvictionCases.csv")

# Filter selected data
data |>
  filter(CASE_ID %in% sullivan$case_id) -> data

# Join to check for correctness
data |>
  select(CASE_ID, WRIT_SERVED, CHANGED_LOCKS) |>
  left_join(sullivan, by = c("CASE_ID" = "case_id")) -> writ_locks

writ_correct <- sum(writ_locks$WRIT_SERVED == writ_locks$writ, na.rm = TRUE)
writ_prop <- writ_correct / length(writ_locks$WRIT_SERVED)
writ_prop

locks_correct <- sum(writ_locks$CHANGED_LOCKS == writ_locks$change_locks, na.rm = TRUE)
locks_prop <- locks_correct / length(writ_locks$WRIT_SERVED)
locks_prop

named_def <- read_csv("../Data/NamedDefendants.csv") |>
  select(CASE_ID, NAMED_DEFENDANTS) |>
  filter( CASE_ID %in% sullivan$case_id ) |>
  group_by(CASE_ID) |>
  nest(data = (NAMED_DEFENDANTS)) |>
  mutate( NAMED_DEFENDANTS = toString(data[1][[1]]$NAMED_DEFENDANTS)) |>
  select(-data)

sullivan |>
  select(case_id, tenants) |>
  mutate(tenants = str_replace_all(as.character(tenants), ";", ",")) |>
  left_join(named_def, by = c("case_id" = "CASE_ID")) -> tenants 

data |>
  select(CASE_ID, DEFENDANTS_ADDRESS) -> address

sullivan |>
  select(case_id, address) |>
  left_join(address, by = c("case_id" = "CASE_ID")) -> address


