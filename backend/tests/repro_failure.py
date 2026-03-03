import json
import os
import sys

# Add the backend directory to the path so we can import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.llm_service import llm_service

def test_repro():
    questions = [
        {"id": "1", "part": "A", "question": "Differentiate between Router and Gateway", "marks": "2"},
        {"id": "2", "part": "A", "question": "If the packet has to go through 3 routers, how many times will encapsulation and decapsulation occur?", "marks": "2"},
        {"id": "3", "part": "A", "question": "List out any three issues in the data link layer", "marks": "2"},
        {"id": "4", "part": "A", "question": "Draw the IEEE 802.3 frame format details", "marks": "2"},
        {"id": "5", "part": "A", "question": "Differentiate between ARP and DHCP protocol", "marks": "2"},
        {"id": "6", "part": "A", "question": "Indicate the Class/type of the following IP addresses: a. 134.53.0.0 b. 1.78.9.2", "marks": "2"}
    ]
    
    # Empty ideal answers to simulate user behavior
    ideal_answers = {}
    
    student_script = """
1. Router: A layer 3 (Network Layer) device that forwards
data packets between different IP networks based on IP
addresses, connecting homogeneous networks.

Gateway: A broader concept, typically operating at higher
layers, that connects two disparate networks, often
performing protocol translation or data format conversion to
facilitate communication between fundamentally different
systems.
While a Router is a specific type of gateway (an IP gateway),
a gateway's functionality extends to encompass wider protocol
& architectural compatibility.

2. When a packet traverses 3 routers, Layer 2 (Data Link Layer)
encapsulation and de-encapsulation will occur 3 times
resulting in a total of 6 such events.
At each of the 3 routers, the incoming Layer 2 frame
is decapsulated to extract the Layer 3 (IP) packet.
After the Router determines the next hop via its routing
table, the Layer 3 packet is then encapsulated
into a new Layer 2 frame with the appropriate
next-hop MAC address for transmission.

3. Here are three issues in the data link layer:
    Error Control: Detecting and correcting transmission error
    (e.g., bit flips) introduced by the physical medium, often using
    mechanisms like (CRC) and (ARQ).
    Flow Control: Managing the data transfer rate between
    Sender and Receiver to prevent buffer overflow at
    the receiving end.
    Medium Access Control (MAC): Regulating access to a
    shared transmission medium by multiple devices to
    prevent collisions and ensure fair, efficient
    channel utilization.

4. The IEEE 802.3 Ethernet frame details the following
    Sequential fields:
    Preamble (7 bytes) and Start Frame Delimiter (SFD) (1 byte)
    for receiver Synchronization
    Destination MAC Address (6 bytes) and Source MAC
    Address (6 bytes) for physical addressing
    Length / Type (2 bytes) indicating the payload length or
    higher - layer protocol type.
    Data and padding (46 - 1500 bytes) containing the
    actual payload, padded to meet minimum frame
    size.

Frame Check Sequence (FCS) (4 bytes) for error detection using a CRC:

5. ARP maps a layer 3 IP address to a layer 2 MAC address within a local network segment, enabling direct delivery between devices. In contrast, DHCP an application layer protocol dynamically assigns IP addresses, subnet masks, default gateways and DNS server information to client devices, facilitating their initial network configuration and connectivity.

6. The IP address 134.53.0.0 belongs to class B. Its first octet (134) falls within the range 128 - 191 characteristic of class B networks.
"""

    print("Running reproduction test...")
    results = llm_service.evaluate_answers(questions, ideal_answers, student_script)
    print("Results:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    test_repro()
