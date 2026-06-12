# DNS Spoofing / DNS Poisoning Attack Lab

> **Laboratorio de Seguridad de Redes — Ataque #3**  
> Instituto Tecnológico de las Américas (ITLA) | Matrícula: 2024-1185

---

## 📋 Descripción

Demostración del ataque **DNS Spoofing combinado con ARP MitM** sobre una red simulada en GNS3. El ataque envenena la tabla ARP de la víctima para interceptar su tráfico DNS y redirigir el dominio `itla.edu.do` hacia una página de login falsa controlada por el atacante, logrando capturar credenciales.

--

---

## Topología de Red

```
  [Kali Linux]          [WebTerm]
  10.11.85.10           10.11.85.20
       |                     |
       +-------[IOU1]--------+
               (Switch)
                  |
               [IOU2]
             10.11.85.1
              (Gateway)
```


<img width="269" height="277" alt="image" src="https://github.com/user-attachments/assets/77ac1318-4162-4ea0-9ac8-a3e6c9a60990" />



| Dispositivo    | Rol        | IP            | Interfaz |
|----------------|------------|---------------|----------|
| Kali Linux     | Atacante   | 10.11.85.10/24 | e0/0    |
| WebTerm        | Víctima    | 10.11.85.20/24 | e0/1    |
| IOU2 (Router)  | Gateway    | 10.11.85.1/24  | e0/2    |
| IOU1 (Switch)  | L2 Switch  | N/A            | Central  |

---

## ⚙️ Requisitos

- GNS3 con imagen IOU L2 (switch) e IOU (router)
- Kali Linux VM (atacante)
- WebTerm VM (víctima)
- Python 3
- Scapy: `pip3 install scapy`
- Flask: `pip3 install flask`

---

## 🚀 Ejecución del Ataque

### 1. Configurar IOU2 (gateway)
```
enable
conf t
interface e0/0
 ip address 10.11.85.1 255.255.255.0
 no shutdown
end
```

### 2. Configurar IP en Kali (atacante)
```bash
ip addr add 10.11.85.10/24 dev eth0
ip link set eth0 up
ip route add default via 10.11.85.1
```

### 3. Configurar IP en WebTerm (víctima)
```bash
ip addr add 10.11.85.20/24 dev eth0
ip link set eth0 up
ip route add default via 10.11.85.1
echo "nameserver 10.11.85.1" > /etc/resolv.conf
```

### 4. Ejecutar los 3 scripts (en terminales separadas)

**Terminal 1 — Servidor web falso:**
```bash
sudo python3 server.py
```

<img width="324" height="89" alt="Captura de pantalla 2026-06-12 164448" src="https://github.com/user-attachments/assets/4f691f23-7aa8-4ef5-aed0-23a3bdcde4be" />

**Terminal 2 — DNS Spoofer:**
```bash
sudo python3 dns_spoof.py
```

<img width="417" height="182" alt="Captura de pantalla 2026-06-12 164512" src="https://github.com/user-attachments/assets/21ebcedd-5f78-4473-864b-bccc9c634433" />

**Terminal 3 — ARP Poisoning:**
```bash
sudo python3 arp_poison.py
```
<img width="424" height="188" alt="Captura de pantalla 2026-06-12 164537" src="https://github.com/user-attachments/assets/7b001a89-0802-4b85-a8ff-3fdd128d6b34" />

### 6. Demostrar el ataque
En el navegador de WebTerm ingresar:
```
http://itla.edu.do
```
<img width="513" height="386" alt="Captura de pantalla 2026-06-12 164559" src="https://github.com/user-attachments/assets/07be2649-7993-40f2-b251-18ab2660c14c" />

---

## Flujo del Ataque

```
WebTerm consulta itla.edu.do
        │
        ▼
Query DNS interceptada por Kali (ARP MitM)
        │
        ▼
dns_spoof.py responde: itla.edu.do = 10.11.85.10
        │
        ▼
WebTerm carga http://10.11.85.10 → Portal falso ITLA
        │
        ▼
Víctima ingresa credenciales → Capturadas en server.py
```

---

##  Demostración

> 📺 Video de demostración: 

---

## 🛡️ Contramedidas

| Ataque | Contramedida |
|--------|-------------|
| ARP Poisoning | Dynamic ARP Inspection (DAI), entradas ARP estáticas |
| DNS Spoofing | DNSSEC, DNS over HTTPS (DoH), DNS over TLS (DoT) |
| Phishing | HTTPS + certificados válidos, MFA, capacitación a usuarios |

---
IOU1# configure terminal
IOU1(config)# ip dhcp snooping
IOU1(config)# ip dhcp snooping vlan 1
IOU1(config)# ip arp inspection vlan 1
IOU1(config)# interface ethernet 0/2
IOU1(config-if)# ip dhcp snooping trust
IOU1(config-if)# ip arp inspection trust
IOU1(config-if)# exit



