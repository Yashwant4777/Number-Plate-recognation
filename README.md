# Vehicle Authentication System using Survillance Camera.
# How is it helpful for mankind?
With the increasing threats to human life its important to cross check with the person who is entering into our vicinity by checking that person's vehicle number in the database and if the number is present in the database then permission is granted and by using arduino and door sensor the door would open.
# How it works?
The application firstly takes input a jpg file(image) or a mp4 file(video) then it convert's the frame to Grey Scale and apply's thresholding to differentiate our vehicle from the background, then by applying contours using canny edge detection of rectangle shape and finding the exact contour which matches the size of our name plate, then noice/unwanted data from the name plate is removed by applying bilateral filter and then Pytesseract tool is used on the resultant image/frame to extract the text/number on the number plate then this number/text is compared with those data which is in out data-base if we find any match then access would be granted else denied.
# Technologies Used:-
The whole application was completely built using Python, computer vision(OpenCV), python tool named Pytesseract and MySQL is used for database.
Hardware used:- Arduino, Door Sensor.
