# Microsat

Ian Francine Demavivas
Galileo Gregory Abrasaldo II
Never gonna give you up!



## Intended Pipeline
#1. Use Fragman R Library to match .fsa file and calibrate with ladder
*From Fragman documentation https://cran.r-project.org/web/packages/Fragman/Fragman.pdf*

>folder <- "~/myfolder"
 
 my.plants <- storing.inds(folder)

>class(my.plants) <- "fsa_stored"
>#Match your ladder
>my.ladder <- c(35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500)
>#Output the ladder-matched file in csv format with the same filename
>for(i in 1:length(my.lad)){
>	write.table(data.frame(my.lad[[i]]), gsub(".fsa", ".csv", names(my.lad)[i]), quote=T, sep=',', col.names=TRUE)
>}

#2. Use python to continue development