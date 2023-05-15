#include "sensors.c"
#include <math.h>
#include <stdlib.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

//Genera el header de un mensaje, con la MAC, el protocolo, status, y el largo del mensaje.
char* header(char protocol, char transportLayer){
	char* head = malloc(12);

    char ID = 'D1'
    memcpy((void*) &(head[0]), (void*) MACaddrs, 2);
	uint8_t* MACaddrs = malloc(6);
	esp_efuse_mac_get_default(MACaddrs);
	memcpy((void*) &(head[2]), (void*) MACaddrs, 6);
    head[8]= transportLayer;
	head[9]= protocol;
	unsigned short dataLen = dataLength(protocol);
	memcpy((void*) &(head[10]), (void*) &dataLen, 2);
	free(MACaddrs);
	return head;
}

unsigned short lengmsg[6] = {2, 6, 16, 20, 44, 12016};
unsigned short dataLength(char protocol){
    return lengmsg[ (unsigned int) protocol]-1;
}

unsigned short messageLength(char protocol){
    return 1+12+dataLength(protocol);
}

char* mensaje (char protocol, char transportLayer){
	char* mnsj = malloc(messageLength(protocol));
	mnsj[messageLength(protocol)-1]= '\0';
	char* hdr = header(protocol, transportLayer);
	char* data;
	switch (protocol) {
		case 0:
			data = dataprotocol00();
			break;
		case 1:
			data = dataprotocol0();
			break;
		case 2:
			data = dataprotocol1();
			break;
		case 3:
			data = dataprotocol2();
			break;
        case 4:
			data = dataprotocol3();
			break;
        case 5:
			data = dataprotocol4();
			break;
		default:
			data = dataprotocol0();
			break;
	}
	memcpy((void*) mnsj, (void*) hdr, 12);
	memcpy((void*) &(mnsj[12]), (void*) data, dataLength(protocol));
	free(hdr);
	free(data);
	return mnsj;
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* dataprotocol00(){
    char* msg = malloc(dataLength(0));
    msg[0] = 1;
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(){
    
    char* msg = malloc(dataLength(1));
    float batt = batt_sensor();
    msg[0] = batt;
    long t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);
    return msg;
}


char* dataprotocol1(){
    
    char* msg = malloc(dataLength(2));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co2();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

    return msg;
}

char* dataprotocol2() {
	char* msg = malloc(dataLength(3));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co2();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

	float rms = RMS();
	memcpy((void*) $(msg[15]), (void*) &rms, 4);

    return msg;
}

char* dataprotocol3() {
	char* msg = malloc(dataLength(4));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co2();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

	float rms = RMS();
	memcpy((void*) $(msg[15]), (void*) &rms, 4);

	float ampx = acc_kpi_amp_x();
	memcpy((void*) $(msg[19]), (void*) &ampx, 4);

	float frecx = acc_kpi_frec_x();
	memcpy((void*) $(msg[23]), (void*) &frecx, 4);

	float ampy = acc_kpi_amp_y();
	memcpy((void*) $(msg[27]), (void*) &ampy, 4);

	float frecy = acc_kpi_frec_y();
	memcpy((void*) $(msg[31]), (void*) &frecy, 4);

	float ampz = acc_kpi_amp_z();
	memcpy((void*) $(msg[35]), (void*) &ampz, 4);

	float frecz = acc_kpi_frec_z();
	memcpy((void*) $(msg[39]), (void*) &frecz, 4);
    return msg;
}

char* dataprotocol4() {
	char* msg = malloc(dataLength(5));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co2();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

	float* acx = acc_sensor_acc_x();
	memcpy((void*) &(msg[15]), (void*) &acx, 8000)

	float* acy = acc_sensor_acc_y();
	memcpy((void*) &(msg[8015]), (void*) &acy, 8000)

	float* acz = acc_sensor_acc_z();
	memcpy((void*) &(msg[16015]), (void*) &acz, 8000)

    return msg;
}

int main() {
    char* a = mensaje(1,1);
    
    for(int i = 0; i < 16; i++) {
        float num = a[i];
        printf("arr[%d] = %f\n",i,num);
    }
    
    free(a);
    return 0;
}