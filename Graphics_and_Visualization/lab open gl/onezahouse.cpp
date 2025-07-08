// Oneza Hassan Alvi (04281913032)

#include <GL/glut.h>

void display()
 {
    
    glClearColor(0.65f, 0.50f, 0.39f, 1.0f);  // brown = background color 


    glClear(GL_COLOR_BUFFER_BIT);


    glLineWidth(2.0f);          // 2.0 = width 
    glColor3f(0.0f, 0.0f, 0.0f); // Black color for the boundry of house
    glBegin(GL_LINE_LOOP);
    glVertex2f(-0.5f, 0.0f);    // Left-bottom vertex
    glVertex2f(0.5f, 0.0f);     // Right-bottom vertex
    glVertex2f(0.5f, 0.5f);     // Top vertex
    glVertex2f(-0.5f, 0.5f);    // Left-top vertex
    glEnd();

    
    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f); // Green color for the roof
    glVertex2f(-0.5f, 0.5f);    
    glVertex2f(0.0f, 0.7f);     
    glVertex2f(0.5f, 0.5f);     
    glEnd();


    glBegin(GL_POLYGON);
    glColor3f(1.0f, 0.5f, 0.8f); // Pink color for the house
    glVertex2f(-0.5f, 0.0f);    
    glVertex2f(0.5f, 0.0f);    
    glVertex2f(0.5f, 0.5f);     
    glVertex2f(-0.5f, 0.5f);    
    glEnd();


    glBegin(GL_QUADS);
    glColor3f(1.0f, 1.0f, 1.0f); // White color for the window
    glVertex2f(-0.1f, 0.1f);   
    glVertex2f(0.1f, 0.1f);     
    glVertex2f(0.1f, 0.3f);     
    glVertex2f(-0.1f, 0.3f);    
    glEnd();  


    glBegin(GL_QUADS);
    glColor3f(0.0f, 0.0f, 1.0f); // Blue color for the door
    glVertex2f(-0.4f, 0.0f);   
    glVertex2f(-0.2f, 0.0f);    
    glVertex2f(-0.2f, 0.3f);    
    glVertex2f(-0.4f, 0.3f);    
    glEnd();


    glBegin(GL_QUADS);
    glColor3f(0.5f, 0.5f, 0.5f); // Grey color for the foot step to house  
    glVertex2f(-0.3f, -0.5f);   
    glVertex2f(0.3f, -0.5f);    
    glVertex2f(0.3f, -0.25f);   
    glVertex2f(-0.3f, -0.25f);  
    glEnd();


    glFlush();
}

int main(int argc, char** argv) 

{
    glutInit(&argc, argv); // GLUT library initialization 
    glutCreateWindow("Oneza House");   // window and title
    glutInitWindowSize(400, 400);   // size of window
    glutInitWindowPosition(100, 100);  // window position on system screen 
    glutDisplayFunc(display); // display callback func
    glutMainLoop();  // looping of glut events
    return 0;
}
// commands to use on MSYS2 MSYS shell
// export PATH=$PATH:/mingw64/bin
// cd /c/Users/DELL/OneDrive/Desktop/graphics
// g++ -o onezahouse onezahouse.cpp -lopengl32 -lglu32 -lfreeglut
// ./onezahouse.exe
