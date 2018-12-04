#!/usr/bin/env python
# -*- coding: utf-8 -*-

def comp_boxes(boxes):
    num_of_boxes = len(boxes)

    for x in range(num_of_boxes):
        for y in range(x, num_of_boxes):
            #print(boxes[x])
            box1 = boxes[x].rstrip()
            box2 = boxes[y].rstrip()
            counter = 0
            if x != y:
                string = ""
                for z in range(len(box1)):
                    if box1[z] == box2[z]:
                        string += box1[z]
                    else:
                        counter += 1
                if counter == 1:
                    print("MATCH")
                    print(box1, " ", box2)
                    return string

f = open('boxes.txt', 'r')
boxes = f.readlines()
f.close()

print(comp_boxes(boxes))