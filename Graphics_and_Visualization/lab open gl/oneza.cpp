#include <GL/glut.h>

void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    glBegin(GL_POLYGON);
    glColor3f(1.0f, 1.0f, 0.0f); // Yellow color
    glVertex2f(-0.5f, 0.0f);    // Left vertex
    glVertex2f(0.5f, 0.0f);     // Right vertex
    glVertex2f(0.5f, 0.5f);     // Top vertex
    glVertex2f(-0.5f, 0.5f);    // Bottom vertex
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f); // Green color
    glVertex2f(-0.6f, 0.5f);    // Left vertex
    glVertex2f(-0.4f, 0.7f);    // Top vertex
    glVertex2f(-0.2f, 0.5f);    // Right vertex
    glEnd();

    glBegin(GL_TRIANGLES);
    glColor3f(0.0f, 1.0f, 0.0f); // Green color
    glVertex2f(0.6f, 0.5f);     // Right vertex
    glVertex2f(0.4f, 0.7f);     // Top vertex
    glVertex2f(0.2f, 0.5f);     // Left vertex
    glEnd();

    glBegin(GL_QUADS);
    glColor3f(0.0f, 0.0f, 1.0f); // Blue color
    glVertex2f(-0.4f, 0.0f);    // Left-bottom vertex
    glVertex2f(-0.2f, 0.0f);    // Right-bottom vertex
    glVertex2f(-0.2f, 0.3f);    // Right-top vertex
    glVertex2f(-0.4f, 0.3f);    // Left-top vertex
    glEnd();

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutCreateWindow("Polygon House");
    glutInitWindowSize(400, 400);
    glutInitWindowPosition(100, 100);
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}

