# AUSOME Microsat

Ian Francine Demavivas
Galileo Gregory Abrasaldo II
Kenneth Kim

## Intended Pipeline
A. Use Fragman R Library to match .fsa file and calibrate with ladder
*from Fragman documentation https://cran.r-project.org/web/packages/Fragman/Fragman.pdf*

1. Assign the directory path.

>folder <- "~/myfolder"  

2. Store the fragment data using the storing.inds() function. set channels=5 since we are using the LIZ-500 dye.  

>my.fragments <- storing.inds(folder,channels=5)  
>  
>class(my.fragments) <- "fsa_stored"

3. Match your ladder  

>matched.ladder <- c(35, 50, 75, 100, 139, 150, 160, 200, 250, 300, 340, 350, 400, 450, 490, 500) 
>ladder.info.attach(stored=my.fragments, ladder=matched.ladder)  
>matched.lad <- list.data.covarrubias #this is where the matched ladder data is stored  

4. Output the ladder-matched file in csv format with the same filename  

>for(i in 1:length(matched.lad)){
>>	write.table(data.frame(matched.lad[[i]]), gsub(".fsa", ".csv", names(matched.lad)[i]), quote=T, sep=',', col.names=TRUE)
>}

>overview2(my.inds=my.plants, channel = 2:3, ladder=matched.ladder, init.thresh=5000)

>(bad codelapply(matched.lad, function(x) write.table(data.frame(x), 'test.csv',quote=T  , append=T, sep=',',col.names=TRUE)))


B. Use Python to continue development