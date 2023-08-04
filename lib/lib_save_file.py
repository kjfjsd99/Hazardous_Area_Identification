import json
import csv
import os

# =============================================================================
#save JSON file result
def saveJSON(outputPath,fileName,person_transform,rectangle_transform,width_transform,height_transform,showProcess=False):
    root_json = {}  
    root_json['people'] = []  

    #add all person
    for (i,coordinate) in enumerate(person_transform):
        #add element in JSON file result
        root_json['people'].append({  
                'name': "person-"+str(i+1),
                'x': coordinate[0],
                'y': coordinate[1]
                })
        #show process
        if showProcess:
            print("Point {} transform: ({},{})".format(str(i),str(coordinate[0]), str(coordinate[1])))
    
    #add transformation coordinate of 4 points (ROI)
    root_json["transformation 4 points (ROI)"] = []
    for (i, coordinate) in enumerate(rectangle_transform):
        #add element in json file result
        root_json["transformation 4 points (ROI)"].append({  
                'name': "corner-"+str(i),
                'x': coordinate[0],
                'y': coordinate[1]
                })
    
    #add size of transform images in JSON file
    root_json["transform image"] = []  
    root_json["transform image"].append({  
            'height': height_transform,
            'width': width_transform
            })
    #save json file result
    fileName = os.path.sep.join([outputPath, fileName+".json"])
    with open(fileName, 'w+') as outfile:  
        json.dump(root_json, outfile)
# =============================================================================
#save CSV file result
def saveCSV(outputPath,fileName,person_transform,rectangle_transform,width_transform,height_transform,showProcess=False):
    fileName = os.path.sep.join([outputPath, fileName+"_transform_CSV.csv"])
    with open(fileName, 'w+', newline='\n') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Person", "x", "y"])
    csvFile.close()

    #add all person
    for (i,coordinate) in enumerate(person_transform):
        #add element in CSV file result
        with open(fileName, 'a+', newline='\n') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([i, coordinate[0], coordinate[1]])
        csvFile.close()
        
        #show process
        if showProcess:
            print("Point {} transform: ({},{})".format(str(i),str(coordinate[0]), str(coordinate[1])))
        
    #add transformation coordinate of 4 points (ROI)
    for (i, coordinate) in enumerate(rectangle_transform):
        #add element in CSV file result
        with open(fileName, 'a+', newline='\n') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["corner-"+str(i), coordinate[0], coordinate[1]])
        csvFile.close()
    
    #add size of transform images in CSV file
    with open(fileName, 'a+', newline='\n') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["transform image (w,h)", width_transform,height_transform])
    csvFile.close()
   
# =============================================================================
#save TXT file result to calculate heatmap
def saveTXT_2(outputPath,fileName,person_transform,rectangle_transform,width_transform,height_transform,showProcess=False):
    enter ="\r\n"
    fileName = os.path.sep.join([outputPath, fileName+"_transform_TXT.txt"])
    f = open(fileName,"w+")
    #POINT DATASET (Persons)
    f.write("#POINT DATASET (Persons)"+enter)
    #get x_person        
    f.write("x=[")
    for (i,coordinate) in enumerate(person_transform):
        if i>0:
            f.write(",")
        f.write(str(coordinate[0])) #x
    f.write("]"+enter)  
     #get y_person        
    f.write("y=[")
    for (i,coordinate) in enumerate(person_transform):
        if i>0:
            f.write(",")
        f.write(str(coordinate[1])) #y
    f.write("]"+enter)  
        
    #POINT RECTANGLE: 0-->1-->2-->3-->0
    f.write("#POINT RECTANGLE: 0-->1-->2-->3-->0"+enter)
    #get x_rectangle        
    f.write("xr=[")
    for (i,coordinate) in enumerate(rectangle_transform):
        if i>0:
            f.write(",")
        f.write(str(coordinate[0])) #x
    f.write("]"+enter)  
     #get y_rectangle        
    f.write("yr=[")
    for (i,coordinate) in enumerate(rectangle_transform):
        if i>0:
            f.write(",")
        f.write(str(coordinate[1])) #y
    f.write("]"+enter)        
    
    #add size of transform images in TXT file
    f.write("transform image (w,h): ("+ str(width_transform)+ ", "+ str(height_transform)+")"+ enter)
    f.close()
    
# =============================================================================
#save TXT file result to calculate heatmap
def saveTXT(outputPath,fileName,person_transform):
    fileName = os.path.sep.join([outputPath, fileName+".txt"])
    f = open(fileName,"w+")
    #get number of people        
    f.write(str(len(person_transform)))
    f.close()
    
# =============================================================================