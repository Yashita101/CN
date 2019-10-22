#include <fstream> 
#include "ns3/core-module.h" 
#include "ns3/point-to-point-module.h" 
#include "ns3/applications-module.h" 
#include "ns3/internet-module.h" 
#include "ns3/flow-monitor-module.h" 
using namespace ns3; 
using namespace std;
NS_LOG_COMPONENT_DEFINE ("Lab1"); 
int main (int argc, char *argv[]) { 
	double lat = 2.0; 
	uint64_t rate = 5000000; 
	double interval = 0.05; 

	NS_LOG_INFO ("Create nodes."); 
	NodeContainer n; 
	n.Create (2); 
	NS_LOG_INFO ("Create channels."); 

	PointToPointHelper p2p; 
	p2p.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (lat)));
	p2p.SetDeviceAttribute ("DataRate", DataRateValue (DataRate (rate))); 
	p2p.SetDeviceAttribute ("Mtu", UintegerValue (1400)); 
	NetDeviceContainer dev = p2p.Install (n.Get(0), n.Get(1));
 
	InternetStackHelper internet; 
	internet.Install (n); 
	Ipv4AddressHelper ipv4; 
	NS_LOG_INFO ("Assign IP Addresses."); 
	ipv4.SetBase ("10.1.1.0", "255.255.255.0"); 
	Ipv4InterfaceContainer i = ipv4.Assign (dev); 

	Ipv4GlobalRoutingHelper::PopulateRoutingTables (); 
	NS_LOG_INFO ("Create Applications."); 

	uint16_t port1 = 8000; 
	UdpServerHelper server1 (port1); 
	ApplicationContainer apps; 
	apps = server1.Install (n.Get (1));  
	apps.Start (Seconds (1.0));
	apps.Stop (Seconds (10.0)); 

	UdpClientHelper client1 (i.GetAddress (1), port1); 
	client1.SetAttribute ("MaxPackets", UintegerValue (320));
	client1.SetAttribute ("Interval", TimeValue (Seconds(interval))); 
	client1.SetAttribute ("PacketSize", UintegerValue (1024)); 

	apps = client1.Install (n.Get (0)); 
	apps.Start (Seconds (2.0)); 
	apps.Stop (Seconds (10.0)); 
	p2p.EnablePcap("lab-1", dev, false); 

	FlowMonitorHelper flowmon;
	Ptr<FlowMonitor> monitor = flowmon.InstallAll();  
	NS_LOG_INFO ("Run Simulation.");
	Simulator::Stop (Seconds(11.0));
	Simulator::Run ();
	monitor->CheckForLostPackets (); 
	Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ( )); 
	map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats (); 
	for (map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i) 
	{ 
	Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first); 
	cout<<" t.sourceAddress="<<t.sourceAddress<<"\n t.destinationAddress="<<t.destinationAddress<<"\n Source port:"<<t.sourcePort<<" \n" <<" Destination port:"<<t.destinationPort<<"\n"; 
	if ((t.sourceAddress=="10.1.1.1" && t.destinationAddress == "10.1.1.2")) 
	{ 
		cout << " Flow " << i->first << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n"; 
		cout << " Tx Bytes: " << i->second.txBytes << "\n"; std::cout << " Rx Bytes: " << i->second.rxBytes << "\n"; 
		cout << " Tx Packets: " << i->second.txPackets << "\n"; std::cout << " Rx Packets: " << i->second.rxPackets << "\n"; std::cout << " Throughput: " << i->second.rxBytes * 8.0 / 9.0 / 					1000 / 1000 << " Mbps\n"; 
}
 
} 
monitor->SerializeToXmlFile("lab-1.flowmon", true, true); 
Simulator::Destroy (); 
NS_LOG_INFO ("Done."); } 

