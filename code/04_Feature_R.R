suppressMessages(library(dplyr))

# functions 
Featurize_train = function(train, encoder_num){
    # numeric
    var_num = names(encoder_num)
    train_var_impute = purrr::map2(train[, var_num], encoder_num, function(.x, .y) ifelse(is.na(.x), .y$impute, .x)) %>% as_tibble(.)
    train_var_scale = purrr::map2(train_var_impute[, var_num], encoder_num, function(.x, .y) (.x - .y$mean)/.y$std ) %>% as_tibble(.)
                                
    X = train_var_scale
    Y = train %>% select(quality)
                               
    return(list(X = X, Y = Y))
}

Featurize_test = function(test, encoder_num){
    # numeric
    var_num = names(encoder_num)
    test_var_impute = purrr::map2(test[, var_num], encoder_num, function(.x, .y) ifelse(is.na(.x), .y[[1]], .x)) %>% as_tibble(.)
    test_var_scale = purrr::map2(test_var_impute[, var_num], encoder_num, function(.x, .y) (.x - .y$mean)/.y$std ) %>% as_tibble(.)
                                  
    X = test_var_scale 
    Y = test %>% select(quality)
                              
    return(list(X = X, Y = Y))
}
                                 
                                 
if (!interactive()){    
    # file and directory info
    ini = commandArgs(trailingOnly = FALSE)
    project_dir = dirname(dirname(sub("--file=", "", ini[grep("--file=", ini)])))
    interim_folder = "/data/interim/"
    processed_folder = "/data/processed/"
    
    # input
    train = arrow::read_parquet(paste0(project_dir, interim_folder, "train.parquet"))
    test = arrow::read_parquet(paste0(project_dir, interim_folder, "test.parquet"))
    encoder_num = readRDS(paste0(project_dir, processed_folder, "encoder_num.rds"))

    # output and save
    feature_train = Featurize_train(train, encoder_num)
    feature_test = Featurize_test(test, encoder_num)
                                  
    arrow::write_parquet(feature_train$X, paste0(project_dir, interim_folder, "train_X.parquet"))
    arrow::write_parquet(feature_train$Y, paste0(project_dir, interim_folder, "train_Y.parquet"))
    arrow::write_parquet(feature_test$X, paste0(project_dir, interim_folder, "test_X.parquet"))
    arrow::write_parquet(feature_test$Y, paste0(project_dir, interim_folder, "test_Y.parquet"))
}
