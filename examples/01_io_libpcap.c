#include "pcap.h"
#include "time.h"

int main(int argc,char *argv[])
{
	char errbuf[PCAP_ERRBUF_SIZE];
	struct pcap_pkthdr *hdr1, hdr2;
	pcap_t *fp = NULL;
	pcap_dumper_t* pDumper = NULL;
	const u_char *pkt_data;
	u_int i=0;
	int res;
	time_t start_time = 0;
	time_t end_time = 0;

	start_time = time(NULL);
	if ((fp = pcap_open_offline(argv[1], errbuf)) == NULL) {
		fprintf(stderr, "\nError opening dump file\n");
		return -1;
	}
	pDumper = pcap_dump_open(fp, argv[2]);
	while((res = pcap_next_ex( fp, &hdr1, &pkt_data)) >= 0){
		pcap_dump((u_char*)pDumper,hdr1, pkt_data);
	}
	pcap_dump_close(pDumper);
	if (fp) pcap_close(fp);
	end_time = time(NULL);
	printf("%s: %ds\n",argv[0],(end_time - start_time));
	return 0;
}
