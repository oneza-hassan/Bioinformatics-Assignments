/*
#include <GL/glut.h>

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0f, 1.0f, 1.0f);
    glPointSize(5.0f);

    glBegin(GL_POINTS);
    glVertex2i(289, 190);
    glVertex2i(320, 128);
    glVertex2i(194, 101);
    glVertex2i(129, 83);
    glVertex2i(75, 73);
    glVertex2i(74, 74);
    glVertex2i(20, 10);
    glEnd();

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutCreateWindow("Big Dipper");
    glutDisplayFunc(display);
    glutMainLoop();
}

*/

/*for large data set we can store the points in the file and then access it using the fstream*/
/*
#include <fstream>
#include <GL/glut.h>
using namespace std;

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glClearColor(0.65f, 0.50f, 0.39f, 1.0f);
    glColor3f(0.0f, 0.0f, 0.0f);
    glPointSize(10.0f);

    ifstream file("bigdipperpoints.txt"); 
    int x, y;
    while (file >> x >> y) {
        glBegin(GL_POINTS);
        glVertex2i(x, y);
        glEnd();
    }

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(640, 480);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, 640, 0, 480);
    glMatrixMode(GL_MODELVIEW);
    glutCreateWindow("Big Dipper");
    glutDisplayFunc(display);
    glutMainLoop();
}

*/

//this prog has some prob will check it later


//PATH=$PATH:/mingw64/bin
//cd /c/Users/DELL/OneDrive/Desktop/graphics/lab\ open\ gl
//g++ -o bigdipper bigdipper.cpp -lopengl32 -lglu32 -lfreeglut                                                                                                       
//./bigdipper.exe
