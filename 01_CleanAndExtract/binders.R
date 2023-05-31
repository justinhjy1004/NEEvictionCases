#===================================================================
# Targeted Binder
# Row binds targeted scraped files 
#===================================================================
library(tidyverse)

# Bind all data
df <- read_csv("../Data/targeted_cases.csv")

df <- df[df$CASE_ID != "CASE_ID",]

# Write CSV
write.csv(df, file = "../Data/targeted_cases.csv", row.names = FALSE)

rm(df)

# Bind all data
df <- read_csv("../Data/bruteforce_cases.csv")

df <- df[df$CASE_ID != "CASE_ID",]

# Write CSV
write.csv(df, file = "../Data/bruteforce_cases.csv", row.names = FALSE)
