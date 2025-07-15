#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dns.resolver
from pyfiglet import Figlet
from termcolor import colored

# Banner bonito
def show_banner():
    f = Figlet(font='slant')
    banner = f.renderText('IP CHECKER')
    print(colored(banner, 'cyan'))
    print(colored("=" * 80, 'blue'))
    print(colored("Tool para verificar IPs en listas negras de seguridad", 'yellow'), colored("By: Enethel Mendoza", 'white'))
    print(colored("=" * 80, 'blue') + "\n")

# Invierte la IP para usarla en consultas DNSBL
def reverse_ip(ip):
    return '.'.join(reversed(ip.strip().split('.')))

# Verifica listas negras
def check_blacklists(ip):
    reversed_ip = reverse_ip(ip)
    
    blacklists = {
        'Spamhaus (ZEN)': f'{reversed_ip}.zen.spamhaus.org',
        'SORBS': f'{reversed_ip}.dnsbl.sorbs.net',
        'Barracuda': f'{reversed_ip}.b.barracudacentral.org',
        'SpamCop': f'{reversed_ip}.bl.spamcop.net',
        'UCEPROTECT': f'{reversed_ip}.dnsbl-1.uceprotect.net'
    }

    results = {}
    for name, query in blacklists.items():
        try:
            answers = dns.resolver.resolve(query, 'A')
            results[name] = [str(r) for r in answers]
        except dns.resolver.NXDOMAIN:
            results[name] = None
        except dns.resolver.NoAnswer:
            results[name] = None
        except dns.resolver.Timeout:
            results[name] = "Timeout"
        except Exception as e:
            results[name] = f"Error: {e}"

    return results

# Main
if __name__ == '__main__':
    show_banner()
    ip = input(colored("[+] Ingresa la IP a verificar: ", 'green'))
    
    print(colored("\n[+] Consultando listas negras...\n", 'magenta'))
    results = check_blacklists(ip)
    
    print(colored("Resultados:", 'yellow', attrs=['bold']))
    for bl, result in results.items():
        if isinstance(result, list):
            status = colored("LISTADA", 'red')
        elif result is None:
            status = colored("No listada", 'green')
        else:
            status = colored("Error", 'yellow')
        print(f"{bl:20} : {status} {str(result) if result else ''}")

    print(colored("\n[*] Consulta completada.\n", 'blue'))
