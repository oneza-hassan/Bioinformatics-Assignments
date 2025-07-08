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
    // a dot is 2 by 2 pixels
    glPointSize(2.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, (GLdouble)screenWidth, 0.0, (GLdouble)screenHeight);
    
    // for sx
    A = screenWidth / 4.0; //a=scaling coeff
    B = 0.0; //b=shifting coeff
    // for sy
    C = D = screenHeight / 2.0; // c and d are scaling and shifting coeff respectively 
}

void myDisplay(void) {
    // clear the screen
    glClear(GL_COLOR_BUFFER_BIT);
    // draw the points
    glBegin(GL_POINTS);
    for (GLdouble x = 0; x < 4.0; x += 0.005) // we took the small step value of 0.005
                                            // so that the ponits are plotted near each other on the graph
        {
        GLdouble func = exp(-x) * cos(2 * 3.14159265 * x);
        glVertex2d(A * x + B, C * func + D); // new points (sx, sy) // on x axis its the original x value
                                            // on y axis its the new function of x values
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
    glutCreateWindow("Dot Plot of a Function");
    // register display function
    glutDisplayFunc(myDisplay);
    myInit();
    // go for a perpetual loop
    glutMainLoop();
}



// export PATH=$PATH:/mingw64/bin
// cd /c/Users/DELL/OneDrive/Desktop/graphics/lab\ open\ gl
// g++ -o dotplot dotplot.cpp -lopengl32 -lglu32 -lfreeglut
// ./dotplot.exe