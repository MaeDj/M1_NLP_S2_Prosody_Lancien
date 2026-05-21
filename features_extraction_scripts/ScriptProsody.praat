############################################
# parameters 
############################################

form Extraction F0
    sentence Fichier_audio C:\Users\mlancien\Desktop\JTTA_Praat-2024-ATILF\COF-002.wav
    sentence Fichier_sortie C:\Users\mlancien\Desktop\JTTA_Praat-2024-ATILF\sortie_F0.txt
endform

pas = 0.015    

############################################
# read wav file 
############################################
Read from file... 'Fichier_audio$' 

sound = selected("Sound")

############################################
# F0 computation
############################################

select sound
To Pitch: 0.0, 75, 300
pitch = selected("Pitch")

duree = Get total duration
nb_pas = floor(duree / pas)

############################################
# write output
############################################

filedelete 'Fichier_sortie$'

fileappend 'Fichier_sortie$' time(s)'tab$'F0(Hz)'newline$'


for i from 0 to nb_pas
    time = i * pas
    select pitch
    f0 = Get value at time: time, "Hertz", "Linear"
    if f0 = undefined
        f0 = 0
    endif
fileappend "'Fichier_sortie$'" 'time''tab$''f0''newline$'
    
endfor

############################################
# clean window
############################################

select sound
Remove
select pitch
Remove

printline "Extraction of F0 all done."
