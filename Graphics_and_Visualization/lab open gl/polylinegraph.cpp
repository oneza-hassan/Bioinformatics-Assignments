#include <math.h>
#include <gl/Gl.h>
#include <gl/glut.h>

// width of the screen window in pixels
const int screenWidth = 640;
// height of the screen window in pixels
const int screenHeight = 480;

// scaling and shifting coefficients
GLdouble A, B, C, D;

void myInit(void) {
    // background color is set to white
    glClearColor(1.0, 1.0, 1.0, 0.0);
    // drawing color is set to black
    glColor3f(0.0f, 0.0f, 0.0f);
    // a dot is 4 by 4 pixels
    glPointSize(4.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, (GLdouble)screenWidth, 0.0, (GLdouble)screenHeight);

    // for sx
    A = screenWidth / 200.0; //a=scaling coeff
    B = 0.0 ; //b=shifting coeff

    // for sy
    C = screenHeight / 1700.0; // c  scaling coeff
    D = screenHeight / 2.0;  //d is the shifting coeff

}

void myDisplay(void) {
    // clear the screen
    glClear(GL_COLOR_BUFFER_BIT);
    // draw the lines
    glBegin(GL_LINE_STRIP);
    for (GLdouble x = 0; x <= 100; x += 3) {
        GLdouble func = 300 - 100 * cos(2 * 3.14 * x / 100) + 30 * cos(4 * 3.14 * x / 100) + 6 * cos(6 * 3.14 * x / 100);
        glVertex2d(A * x + B, C * func + D);  // new points (sx, sy)
    }
    glEnd();
    glFlush();
}

int main(int argc, char** argv) {
    // initialize the toolkit
    glutInit(&argc, argv);
    // set display mode
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    // set window size
    glutInitWindowSize(screenWidth, screenHeight);
    // set window position on screen
    glutInitWindowPosition(100, 150);
    glutCreateWindow("Line Plot of a Function");
    // register display function
    glutDisplayFunc(myDisplay);
    myInit();
    // go for a perpetual loop
    glutMainLoop();
}

//PATH=$PATH:/mingw64/bin
//cd /c/Users/DELL/OneDrive/Desktop/graphics/lab\ open\ gl
//g++ -o polylinegraph polylinegraph.cpp -lopengl32 -lglu32 -lfreeglut
//./polylinegraph.exe


