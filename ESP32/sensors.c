#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
//#include "esp_system.h"
//#include "esp_mac.h"
//#include "esp_log.h"
//int num = (rand() %
//        (upper - lower + 1)) + lower;
/*

Aqui generamos los 5 tipos de protocolos con sus datos.
Las timestamps en realidad siempre mandamos 0, y por comodidad 
guardamos la timestampo del tiempo de llegada en el servidor de la raspberry.


En general los "mensajes" los creamos copiando a la mala (con memcpy) la memoria de los datos en un char*.
No es muy elegante pero funciona.

Al final lo único que se usa fuera de este archivo es:

message: dado un protocolo, crea un mensaje (con header y datos) codificado en un array de bytes (char*).
messageLength: dado un protocolo, entrega el largo del mensaje correspondiente

*/




float floatrand(float min, float max){
    return min + (float)rand()/(float)(RAND_MAX/(max-min));
}


float* acc_sensor_acc_x(){
    double r;
    double x;
    float* arr = malloc(2000* sizeof(float));
    int found = 0;
    
    for (int i =0; i <2000; i++){
        float d = floatrand(-8000, 8000);
        if (arr[i] == d) {
            found = 1;
            while(found) {
                float d = floatrand(-8000, 8000);
                found = 0;
                for (int j = 0; j < 2000; j++) {
                    if (arr[j] == d) {
                        found = 1;
                        break;
                    }
                }
                arr[i] = 2 * sin(2*M_PI*0.001*d);
            }

        }
        else {
            arr[i] = 2 * sin(2*M_PI*0.001*d);
        }
    }
    return arr;
}

float* acc_sensor_acc_y(){
    double r;
    double x;
    float* arr = malloc(2000* sizeof(float));
    int found = 0;
    
    for (int i =0; i <2000; i++){
        float d = floatrand(-8000, 8000);
        if (arr[i] == d) {
            found = 1;
            while(found) {
                float d = floatrand(-8000, 8000);
                found = 0;
                for (int j = 0; j < 2000; j++) {
                    if (arr[j] == d) {
                        found = 1;
                        break;
                    }
                }
                arr[i] = 3 * cos(2*M_PI*0.001*d);
            }

        }
        else {
            arr[i] = 3 * cos(2*M_PI*0.001*d);
        }
    }
    return arr;
}

float* acc_sensor_acc_z(){
    double r;
    double x;
    float* arr = malloc(2000* sizeof(float));
    int found = 0;
    
    for (int i =0; i <2000; i++){
        float d = floatrand(-8000, 8000);
        if (arr[i] == d) {
            found = 1;
            while(found) {
                float d = floatrand(-8000, 8000);
                found = 0;
                for (int j = 0; j < 2000; j++) {
                    if (arr[j] == d) {
                        found = 1;
                        break;
                    }
                }
                arr[i] = 10 * sin(2*M_PI*0.001*d);
            }

        }
        else {
            arr[i] = 10 * sin(2*M_PI*0.001*d);
        }
    }
    return arr;
}


unsigned char THPC_sensor_temp(){
    //int n = (rand() %25) + 5;
    unsigned char n = (unsigned char)floatrand(5,30);
    return n;
}

unsigned char THPC_sensor_hum(){
    unsigned char n = (unsigned char)floatrand(30,80);
    return n;
}

int THPC_sensor_pres(){
    //int n = (rand() %25) + 5;
    int n = (int)floatrand(1000,1200);
    return n;
}

float THPC_sensor_co2(){
    float n = floatrand(30,200);
    return n;
}

int batt_sensor(){
    int n = (int)floatrand(1,100);
    return n;
}

float acc_kpi_amp_x() {
    float n = floatrand(0.0059,0.12);
    return n;
}

float acc_kpi_frec_x() {
    float n = floatrand(29,31);
    return n;
}

float acc_kpi_amp_y() {
    float n = floatrand(0.0041,0.11);
    return n;
}

float acc_kpi_frec_y() {
    float n = floatrand(59,61);
    return n;
}

float acc_kpi_amp_z() {
    float n = floatrand(0.008,0.15);
    return n;
}

float acc_kpi_frec_z() {
    float n = floatrand(89,91);
    return n;
}

float RMS() {
    float x = acc_kpi_amp_x();
    float y = acc_kpi_amp_y();
    float z = acc_kpi_amp_z();
    float res = sqrt((x*x) + (y*y) + (z*z));
    return res;
}

int main() {
    float* a = acc_sensor_acc_x();
    
    for(int i = 0; i < 2000; i++) {
        float n = RMS();
        float num = a[i];
        printf("int(%f)\n",n);
        //printf("arr[%d] = %f\n",i,num);
    }
    
    free(a);
    return 0;
}