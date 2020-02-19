suppressMessages(library(dplyr))

# functions
Encoder_numeric = function(train, num_variables, method){
    train_num = train %>% select(!!!num_variables)
    
    summary_mean = train_num %>% summarise_at(num_variables, mean, na.rm = TRUE)
    summary_std = train_num %>% summarise_at(num_variables, sd, na.rm = TRUE)

    if (method == "mean") {
        summary_num = summary_mean
    }
    if (method == "median") {
         summary_num = train_num %>% summarise_at(num_variables, median, na.rm = TRUE)
    }
    
    summary_num_list = list()
    for (i in 1:ncol(summary_num)){
        col_name = names(summary_num)[i]
        summary_num_list[[i]] = data.frame(mean = as.numeric(summary_mean[,col_name]), 
                                           std = as.numeric(summary_std[,col_name]), 
                                           impute = as.numeric(summary_num[,col_name]))
        
    }
    names(summary_num_list) = names(summary_num)
    
    return(summary_num_list)
}

if (!interactive()){
    args = commandArgs(trailingOnly = TRUE)
    method = args[1]
    
    # file and directory info
    ini = commandArgs(trailingOnly = FALSE)
    project_dir = dirname(dirname(sub("--file=", "", ini[grep("--file=", ini)])))
    interim_folder = "/data/interim/"
    processed_folder = "/data/processed/"
    
    # input
    train = arrow::read_parquet(paste0(project_dir, interim_folder, "train.parquet"))
    num_variables = train %>% select(-quality) %>% names(.)
    
    # output and save
    encoder_num = Encoder_numeric(train, num_variables, method)
    saveRDS(encoder_num, paste0(project_dir, processed_folder, "encoder_num.rds"))
}
