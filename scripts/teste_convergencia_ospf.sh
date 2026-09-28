#!/bin/bash

RESULTADO="resultados/ospf/convergencia.txt"
INTERFACE="eth1"
TIMEOUT=60

# Restaura o enlace mesmo se o script for interrompido
restaurar() {
    docker exec R3 ip link set "$INTERFACE" up >/dev/null 2>&1
}

trap restaurar EXIT INT TERM

echo "=== Teste de convergência OSPF ===" | tee "$RESULTADO"
echo "Falha simulada: enlace R3-R5 (R3 eth1 / 10.0.35.2)" | tee -a "$RESULTADO"
echo "Ponto de observação: tabela de roteamento do R3" | tee -a "$RESULTADO"
echo "Rota alternativa esperada: via R4 (10.0.34.3)" | tee -a "$RESULTADO"
echo | tee -a "$RESULTADO"

echo "Rota antes da falha:" | tee -a "$RESULTADO"
docker exec R3 vtysh -c "show ip route 192.168.5.0/24" 2>/dev/null | tee -a "$RESULTADO"
echo | tee -a "$RESULTADO"

echo "Derrubando enlace R3-R5..." | tee -a "$RESULTADO"

INICIO=$(date +%s%N)

docker exec R3 ip link set "$INTERFACE" down

while true; do

    ROTA=$(docker exec R3 vtysh -c "show ip route 192.168.5.0/24" 2>/dev/null)

    if echo "$ROTA" | grep -q "10.0.34.3"; then

        FIM=$(date +%s%N)
        TEMPO=$(( (FIM - INICIO) / 1000000 ))

        echo | tee -a "$RESULTADO"
        echo "Rota alternativa instalada:" | tee -a "$RESULTADO"
        echo "$ROTA" | tee -a "$RESULTADO"
        echo | tee -a "$RESULTADO"
        echo "Tempo de convergência: $TEMPO ms" | tee -a "$RESULTADO"

        break
    fi

    AGORA=$(date +%s%N)
    DECORRIDO=$(( (AGORA - INICIO) / 1000000 ))

    if [ "$DECORRIDO" -ge $((TIMEOUT * 1000)) ]; then

        echo | tee -a "$RESULTADO"
        echo "ERRO: rota alternativa não encontrada após ${TIMEOUT}s." | tee -a "$RESULTADO"
        echo "$ROTA" | tee -a "$RESULTADO"

        break
    fi

    sleep 0.1

done

echo | tee -a "$RESULTADO"
echo "Restaurando enlace R3-R5..." | tee -a "$RESULTADO"

restaurar
trap - EXIT INT TERM

echo "Enlace restaurado." | tee -a "$RESULTADO"
echo "Resultado salvo em $RESULTADO"
