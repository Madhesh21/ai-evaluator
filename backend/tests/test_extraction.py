import sys
import os
import json

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_service import llm_service

# Mock text based on the user's images
mock_text = """
Roll No. 2 0 2 3 1 1 7 9 0 5 7
ANNA UNIVERSITY (UNIVERSITY DEPARTMENTS)
M.C.A(Regular & Self Supporting)
END SEMESTER EXAMINATIONS JANUARY 2024
CA3104-COMPUTER NETWORKS AND MANAGEMENT
(Regulation 2023)
Time: 3hrs Max.Marks: 100
PART- A (10 x 2 = 20 Marks)
(Answer all Questions)
Q. No Questions Marks CO BL
1 Differentiate between Router and Gateway. 2 CO1 L1
2 If the packet has to go through 3 routers, how many times will encapsulation and decapsulation take place? 2 CO1 L3
3 List out any three issues in the data link layer. 2 CO2 L1
4 Draw the IEEE 802.3 frame format. 2 CO2 L1
5 Differentiate between ARP and DHCP protocol. 2 CO3 L2
6 Indicate the Class/type of the following IP addresses: 2 CO3 L3
a. 134.53.0.0
b. 1.78.9.23
7 How TCP provide reliable data delivery? Justify your answers. 2 CO4 L1
8 Describe the various part of HTTP. 2 CO4 L3
9 List out some open source network monitoring tools. 2 CO5 L1
10 Mention few points about Software Defined Network. 2 CO5 L2

PART- B (5 x 13 = 65 Marks)
(Restrict to a maximum of 2 subdivisions)
Q. No Questions Marks CO BL
11 a i) Explain in brief about various layers of OSI reference model and mention the functions of each layer with suitable sketches (10) ii) what are the various delays occurred in networks? (3) 13 CO1 L2
OR
11 (b) (i) Discuss the TCP/IP model with suitable sketches. 7 CO1 L2
(ii) Explain in brief about various topologies in network arrangement. 6
12 (a) i) Given a CRC polynomial of x3+x2+1, calculate the CRC that is transmitted for a data pattern of 10101101. If an error occurs in the most significant bit of the data, show how it will be detected (9) 13 CO2 L4
ii) Give an example to show two-dimensional parity can correct 1 bit error (4)
OR
12 (b) i) Explain in Brief about the access method and frame format used in IEEE 802.3 with suitable sketches (9) 13 CO2 L4
ii)How does a CSMA/CD used in MAC? (4).
13 a) i)Explain the various fields in the header format of IP datagram (8) 13 CO3 L3
ii) Consider the IP address 128.33 allotted to office. create four subnets with equal size. Write the subnet mask number, subnet number, number of hosts, starting IP, last IP address of all four subnets in tabular column format.(5)
OR
13 (b) i) What are the three types of autonomous systems used with BGP and what are their properties and explain in brief about Inter-domain routing using BGP protocol (8) 13 CO3 L3
ii) Discuss the salient features of IPv6. (5)
14 (a) (i) i) Define the three-way handshake of the TCP initialization protocol in detail, using Time outs. Explain how it avoids misunderstandings caused by a delayed Packet. (7) 13 CO4 L4
ii) Explain briefly about HTTP protocol with suitable sketches (6)
OR
14 (b) i)Write short notes on User Datagram Protocol and discuss the various fields of UDP Datagram header with neat sketches. (7) 13 CO4 L4
ii) Explain the steps involved in DNS look-up for the web-site www.annauniv.edu with recursive and iterative requests, along with the details of the messages exchanged (6)
15 (a) How you use Wireshark tool to explore, analyse and filter the packet transmission in a network? Explore and analyse any 4 protocols using Wireshark tool. 13 CO5 L5
OR
15 (b) (i) Explain briefly about SNMP protocol for network management effectively. 7 CO5 L5
(ii) Mention the use of control plane and data plane in SDN. 6

PART- C (1 x 15 = 15 Marks)
(Q.No.16 is compulsory)
Q. No Questions Marks CO BL
16. (i) Using link state and distance vector protocol show how the routing table would be constructed at node B in the figure given below. 15 CO3 L3, L5
[Diagram: A network graph with nodes A, B, C, D, E and weighted edges]
"""

def test_extraction():
    print("Starting extraction test...")
    questions = llm_service.extract_questions(mock_text)
    
    print(f"\nExtracted {len(questions)} questions.")
    
    # We expect Part A (10) + Part B (5 pairs of OR = 10) + Part C (1) = 21 questions total if all options are extracted.
    # The user said there are 15 questions, probably referring to the main numbers 1-16 (11-15 being 5).
    # If 11(a) and 11(b) are separate, it's more.
    
    for q in questions:
        print(f"ID: {q.get('id')}, Marks: {q.get('marks')}, CO: {q.get('co')}, BL: {q.get('bl')}")
        # print(f"Question: {q.get('question')[:50]}...")
    
    ids = [str(q.get('id')) for q in questions]
    print(f"\nExtracted IDs: {ids}")
    
    # Check if 1-10 are present
    part_a_missing = [str(i) for i in range(1, 11) if str(i) not in ids]
    if part_a_missing:
        print(f"FAILED: Part A questions missing: {part_a_missing}")
    else:
        print("SUCCESS: Part A (1-10) extracted correctly.")
        
    # Check if Part B components are present
    part_b_ids = [id for id in ids if id.startswith('11') or id.startswith('12') or id.startswith('13') or id.startswith('14') or id.startswith('15')]
    print(f"Part B IDs found: {part_b_ids}")
    
    # Check if 16 is present
    if any(id.startswith('16') for id in ids):
        print("SUCCESS: Part C (16) extracted correctly.")
    else:
        print("FAILED: Part C (16) missing.")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.")
    else:
        test_extraction()
