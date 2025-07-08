// oneza Hassan Alvi (04282913032)

#include <math.h>
#include <GL/gl.h>
#include <GL/glut.h> // glut library for creating windows and handling other events

const int screenWidth = 600;
const int screenHeight = 480;

GLdouble A, B, C, D; // global variables of type GLdouble

void myInit(void) {  // initialization func
    glClearColor(1.0, 0.5, 0.5, 0.0); // pink background window
    glColor3f(0.0, 0.0, 0.0);  // black drawing color
    glPointSize(2.0);   // 2.0 pixel point size
    glMatrixMode(GL_PROJECTION); // current matrix is set to projection matrix
    glLoadIdentity();
    gluOrtho2D(0.0, (GLdouble)screenWidth, 0.0, (GLdouble)screenHeight);

    // set the scalling & translation factors
    A = screenWidth / 100.0;  // SF for x axis
    B = 0.0;   //TF for x axis
    C = screenHeight / 500.0;  //SF for y axis
    D = screenHeight / 500.0; //TF for y axis
}

void myDisplay(void) {  // display func
    glClear(GL_COLOR_BUFFER_BIT);
    glBegin(GL_LINE_STRIP);  // start drawing a connected line segment
    for (GLdouble x = 0; x <= 100.0; x += 3.0) {
        // loop through x values from 0 to 100 and have 3.0 as a step function 
        // calculate the function value at x 
        GLdouble func = 300.0 - 100.0 * cos(2 * 3.14159265 * x / 100.0) + 30.0 * cos(4 * 3.14159265 * x / 100.0) + 6.0 * cos(6 * 3.14159265 * x / 100.0);
        // scale and translate x and y values and draw a vertex
        glVertex2d(A * x + B, C * func + D);
    }
    glEnd();
    glFlush();
}

int main(int argc, char **argv) {
    glutInit(&argc, argv); 
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB); // display mode set to single buffer and RGB color model values
    glutInitWindowSize(screenWidth, screenHeight); // size of window
    glutInitWindowPosition(100, 150); // position of window
    glutCreateWindow("Line Graph of a Function");  // window and its title
    glutDisplayFunc(myDisplay); // register display call back func
    myInit(); //call initialization (ie init) func
    glutMainLoop(); // eneter main loop and handle events
    return 0;
}




// commands to use on MSYS2 MSYS shell
// export PATH=$PATH:/mingw64/bin
// cd /c/Users/DELL/OneDrive/Desktop/graphics
// g++ -o task2oneza task2oneza.cpp -lopengl32 -lglu32 -lfreeglut
// ./task2oneza.exe

