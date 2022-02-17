# **<a name="image" />Image**

    class Image():

Objective : create the image to print with pygame. There are 8 types of box with 8 different color :

Attributs  | Color
--- | ---
`start` | [blue](../images/blue_box.png)
`evaluated` | [red](../images/red_box.png)
`nonEvaluated` | [green](../images/green_box.png)
`end` | [orange](../images/orange_box.png)
`wall` | [black](../images/black_box.png)
`empty` | [grey](../images/grey_box.png)
`path` | [cyan](../images/cyan_box.png)
`current` | [pink](../images/pink_box.png)

Find the images used for the boxes the *images* folder 

## **Constructor**

    def __init__(self, width, height):

Parameter | Use
--- | ---
width | the width of the image
height | the height of the image