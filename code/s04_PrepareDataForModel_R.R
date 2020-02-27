suppressMessages(library(dplyr))

# functions 
PrepareData = function(data, encoder_num, var_y){
    # numeric variables
    var_num = names(encoder_num)
    # impute missing values with known value
    data_var_impute = purrr::map2(data[, var_num], encoder_num, function(.x, .y) ifelse(is.na(.x), .y$impute, .x)) %>% 
                                  as_tibble(.)
    # normalized data with known mean and std
    data_var_scale = purrr::map2(data_var_impute[, var_num], encoder_num, function(.x, .y) (.x - .y$mean)/.y$std ) %>% 
                                 as_tibble(.)
                                
    X = data_var_scale
                                 
    # response variable
    if (is.null(var_y)){
        return(list(X = X))
    } else {
        Y = data %>% select(!!!var_y)
        return(list(X = X, Y = Y))
    }
}                            
                                 
if (!interactive()){  
    args = commandArgs(trailingOnly = TRUE)
    ini = commandArgs(trailingOnly = FALSE)
    data_name = args[1]
    type = args[2]
    
    # file and directory info
    project_dir = dirname(dirname(sub("--file=", "", ini[grep("--file=", ini)])))
    
    if (type == "train"){
        interim_folder = "/data/interim/"
        processed_folder = "/data/processed/"
        
        data_path = interim_folder
        encoder_path = processed_folder
    } else if (type == "pred"){
        tmp_folder = "/tmp/"
        artifacts_folder = "/artifacts/"
        
        data_path = tmp_folder
        encoder_path = artifacts_folder
    } else {
         stop('the value for args[2] is not supported.')
    }   
    
    # input
    data = arrow::read_parquet(paste0(project_dir, data_path, data_name))
    encoder_num = jsonlite::fromJSON(paste0(project_dir, encoder_path, "encoder_num.json")) %>% 
        jsonlite::fromJSON(.)

    # output and save
    var_y = "quality"
    if (!var_y %in% names(data)){
        var_y = NULL
    }
    feature_data = PrepareData(data, encoder_num, var_y = var_y)
    name = unlist(strsplit(data_name, "[.]"))[1] 
    
    arrow::write_parquet(feature_data$X, paste0(project_dir, data_path, name, "_X.parquet"))
    if (length(feature_data) > 1){
        arrow::write_parquet(feature_data$Y, paste0(project_dir, data_path, name, "_Y.parquet"))
    }
}
    
    
