# 🎯 DNS Spoofing / DNS Poisoning Attack Lab

> **Laboratorio de Seguridad de Redes — Ataque #3**  
> Instituto Tecnológico de las Américas (ITLA) | Matrícula: 2024-1185

---

## 📋 Descripción

Demostración del ataque **DNS Spoofing combinado con ARP MitM** sobre una red simulada en GNS3. El ataque envenena la tabla ARP de la víctima para interceptar su tráfico DNS y redirigir el dominio `itla.edu.do` hacia una página de login falsa controlada por el atacante, logrando capturar credenciales.

---

## 🗂️ Estructura del Repositorio

```
dns-spoofing/
├── arp_poison.py      # Script de envenenamiento ARP (MitM)
├── dns_spoof.py       # Script de DNS Spoofing (intercepta queries DNS)
├── server.py          # Servidor Flask con portal de login falso
├── index.html         # Réplica visual del portal de login de ITLA
└── README.md
```

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

### 4. Clonar el repositorio en Kali
```bash
git clone https://github.com/TU_USUARIO/dns-spoofing.git
cd dns-spoofing
```

### 5. Ejecutar los 3 scripts (en terminales separadas)

**Terminal 1 — Servidor web falso:**
```bash
sudo python3 server.py
```

**Terminal 2 — DNS Spoofer:**
```bash
sudo python3 dns_spoof.py
```

**Terminal 3 — ARP Poisoning:**
```bash
sudo python3 arp_poison.py
```

### 6. Demostrar el ataque
En el navegador de WebTerm ingresar:
```
http://itla.edu.do
```

---

## 🔄 Flujo del Ataque

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

## 📸 Demostración

> 📺 Video de demostración: [Ver en YouTube](https://youtube.com/TU_ENLACE)

---

## 🛡️ Contramedidas

| Ataque | Contramedida |
|--------|-------------|
| ARP Poisoning | Dynamic ARP Inspection (DAI), entradas ARP estáticas |
| DNS Spoofing | DNSSEC, DNS over HTTPS (DoH), DNS over TLS (DoT) |
| Phishing | HTTPS + certificados válidos, MFA, capacitación a usuarios |

---

## ⚠️ Aviso Legal

Este laboratorio fue desarrollado con fines **exclusivamente educativos** en un entorno controlado y simulado (GNS3). El uso de estas técnicas fuera de un entorno de laboratorio autorizado es ilegal y contrario a la ética profesional.

---

## 👤 Autor

**Estudiante:** Eunice  
**Matrícula:** 2024-1185  
**Institución:** Instituto Tecnológico de las Américas (ITLA)  
**Curso:** Seguridad de Redes
