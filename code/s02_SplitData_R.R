suppressMessages(library(dplyr))

# functions
SplitData = function(raw_data, random_seed, percent_train){
    set.seed(random_seed)
    
    train_index = sample(1:nrow(raw_data), percent_train * nrow(raw_data))
    test_index = setdiff(1:nrow(raw_data), train_index)

    train = raw_data[train_index, ]
    test = raw_data[test_index, ]
    
    return(list(train = train, test = test))
}

if (!interactive()){
    
    args = commandArgs(trailingOnly = TRUE)
    random_seed = as.numeric(args[1])
    percent_train = as.numeric(args[2])
    
    # file and directory info
    file_name = 'winequality-red.csv'
    ini = commandArgs(trailingOnly = FALSE)
    project_dir = dirname(dirname(sub("--file=", "", ini[grep("--file=", ini)])))
    raw_folder = "/data/raw/"
    interim_folder = "/data/interim/"

    # input
    raw_data = data.table::fread(paste0(project_dir, raw_folder, file_name), fill = TRUE) %>%
        dplyr::as_tibble(.)

    # ouptut and save
    train_test = SplitData(raw_data, random_seed, percent_train)
    arrow::write_parquet(train_test$train, paste0(project_dir, interim_folder, "train.parquet"))
    arrow::write_parquet(train_test$test, paste0(project_dir, interim_folder, "test.parquet"))
}