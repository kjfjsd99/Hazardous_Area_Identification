from xml.etree import ElementTree
import cv2

# =============================================================================
# convert bounding box of person --> to coordinate of person, and change ratio
def convertPersonCoordinate(bboxes_person, width_input, width_output): # current: bboxes_person in width_input
    ratio = width_input/width_output
    person=[] #list of person
    for (i, itembox) in enumerate(bboxes_person): 
        (ymin, xmin, ymax, xmax) = itembox #get bbox
        #covert to original codinate
        ymin = int(ymin/ratio)
        xmin = int(xmin/ratio)
        ymax = int(ymax/ratio)
        xmax = int(xmax/ratio)
        person.append([int(xmin) + int((xmax-xmin)/2), int(ymax) - int((ymax-ymin)*0.3)])
    return person

# =============================================================================
# read XML file of person
def readPersonCoordinate(fileXML_person):
    tree_person = ElementTree.parse(fileXML_person)
    root_person = tree_person.getroot()
    person=[] #list of person
    for i,objects in enumerate(root_person.findall('object')):
        #name = objects.find('name').text
        xmin = objects.find('bndbox').find("xmin").text
        xmax = objects.find('bndbox').find("xmax").text
        ymax = objects.find('bndbox').find("ymax").text
        person.append([int((int(xmax)-int(xmin))/2)+int(xmin), int(ymax)])
    return person
    
# =============================================================================
# read XML file of 4 points (ROI)
def readRoICoordinate(fileXML_4points):
    tree_4points = ElementTree.parse(fileXML_4points)
    root_4points = tree_4points.getroot()
    point_rectangle=[] #list of 4 points reference (ROI)
    for i,objects in enumerate(root_4points.findall('object')):
        #name = objects.find('name').text
        xmin = objects.find('bndbox').find("xmin").text
        ymin = objects.find('bndbox').find("ymin").text
        xmax = objects.find('bndbox').find("xmax").text
        ymax = objects.find('bndbox').find("ymax").text
        point_rectangle.append([int(xmin), int(ymin), int(xmax), int(ymax)])
    return point_rectangle

# =============================================================================
#function: convert to tuple (type of point)
def getRoI(point_rectangle):
    rec_0= tuple([point_rectangle[0][0],point_rectangle[0][1]])
    rec_1= tuple([point_rectangle[1][0],point_rectangle[1][1]])
    rec_2= tuple([point_rectangle[2][0],point_rectangle[2][1]])
    rec_3= tuple([point_rectangle[3][0],point_rectangle[3][1]])
    return rec_0,rec_1,rec_2,rec_3

# =============================================================================
#function: get point perspective
def pointPerspective(point,matrix):
    px = (matrix[0][0]*point[0] + matrix[0][1]*point[1] + matrix[0][2]) / ((matrix[2][0]*point[0] + matrix[2][1]*point[1] + matrix[2][2]))
    py = (matrix[1][0]*point[0] + matrix[1][1]*point[1] + matrix[1][2]) / ((matrix[2][0]*point[0] + matrix[2][1]*point[1] + matrix[2][2]))
    return(int(px), int(py))
# =============================================================================
#function: get list of point perspective
def listPerspective(list,matrix):
    list_transform = []
    for coordinate in list: #list=[[x0,y0], [xi,yi],...] - list of list
        point= tuple([coordinate[0],coordinate[1]]) #list --> tuple
        #get transformation point: list_transform = [(x0,y0), (xi, yi), ...] - list of tuple
        point_transform = pointPerspective(point,matrix)
        list_transform.append(point_transform)
    return list_transform

# =============================================================================
#function: draw rectangle (bounding box) from 4 ponits
def drawRectangle(image,p0,p1,p2,p3, color=(0,0,255), size=2):
    cv2.line(image,p0,p1,color,size)
    cv2.line(image,p1,p2,color,size)
    cv2.line(image,p2,p3,color,size)
    cv2.line(image,p3,p0,color,size)