#import the necessary packages
# =============================================================================
#compute the intersection over union 
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    #bbox = [startY, startX, endY, endX]
    y1 = max(boxA[0], boxB[0])
    x1 = max(boxA[1], boxB[1])
    y2 = min(boxA[2], boxB[2])
    x2 = min(boxA[3], boxB[3])
 
    # compute the area of intersection rectangle
    interArea = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
 
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
 
    # return the intersection over union value
    return iou

# =============================================================================
#compute the intersection over max(boxA, boxB)
def bb_belong(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    x1 = max(boxA[0], boxB[0])
    y1 = max(boxA[1], boxB[1])
    x2 = min(boxA[2], boxB[2])
    y2 = min(boxA[3], boxB[3])
 
    # compute the area of intersection rectangle
    interArea = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
 
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iouA = interArea / float(boxAArea)
    iouB = interArea / float(boxBArea)
    if iouA>=iouB: iou=iouA
    else: iou=iouB
    
    # return the intersection over union value
    return iou

# =============================================================================    
#combine boxA & boxB 
def union(boxA, boxB):
    #bbox = [startY, startX, endY, endX]
    y1 = min(boxA[0], boxB[0])
    x1 = min(boxA[1], boxB[1])
    y2 = max(boxA[2], boxB[2])
    x2 = max(boxA[3], boxB[3])
 
    # return the intersection over union value
    return [y1,x1,y2,x2]

# =============================================================================
#combine boxA & boxB 
def check_empty(list_bboxes,status_list_bboxes):
    empty = True
    for i, box in enumerate(list_bboxes): #status of box is true
        if status_list_bboxes[i]==True:
            empty = False
            break
    return empty

# =============================================================================