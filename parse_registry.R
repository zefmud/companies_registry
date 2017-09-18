library(XML)
library(stringr)

on_end <- function(name) {
  if (name == "FOUNDER") {
    list_from_xml[[name]] <<- c(list_from_xml[[name]], content_g)
  } else {
    if (name %in% headers) {
      list_from_xml[name] <<- content_g
    } else {
      if (name == "RECORD") {
        if (length(list_from_xml[['FOUNDER']]) == 0) {
          list_from_xml[['FOUNDER']] <- ''
        }
        df_temp <- data.frame(list_from_xml)
        xml_df <<- rbind(xml_df, df_temp)
        if (nrow(xml_df) >  10000) {
          filepath <- paste0(folder, paste0( as.character(count), ".csv"))
          write.csv(xml_df, filepath, row.names = FALSE)
          xml_df <<- data.frame()
          count <<- count + 1
        }
        list_from_xml[['FOUNDER']] <<- character()

      } else {
        if (name == "DATA") {
          filepath <- paste0(folder, paste0( as.character(count), ".csv"))
          write.csv(xml_df, filepath, row.names = FALSE)
        }
      }
    }
  }

}

gather_folder <- function(folder) {
  files <- list.files(folder)
  df <- data.frame()
  for (f in files) {
    print(f)
    df <- rbind(df, read.csv(paste0(folder,f)))
  }
  df
}

headers <- c('NAME', 'SHORT_NAME', 'EDRPOU', 'ADDRESS', 'BOSS', 'KVED', 'STAN', "FOUNDER")
filename <- "15.1-EX_XML_EDR_UO.xml"
folder <- "csvs/"
list_from_xml <- list()
for (h in headers) {
  list_from_xml[h] <- character()
}
file_number <- 1
count <- 1
el <- NULL
content_g <- ""
name_g <- ""
xml_df <- data.frame()
xmlEventParse(file = filename,
                    list(startElement = function(name, atts) {content_g <<- ''; name_g <<- name},
                         text = function(content){
                           if ((name_g) == "KVED") {
                             content_g <<- str_trim(paste(content_g, content))
                           } else {
                             content_g <<- str_trim(paste(content_g, content))
                           }
                         },
                         endElement = on_end))
write.csv(list_from_xml, paste0(  folder, as.character(file_number), ".csv"), row.names = FALSE)
print("gathering in single csv")
csv_from_xml  <- gather_folder(folder)
write.csv(csv_from_xml, paste0(filename, ".csv"))