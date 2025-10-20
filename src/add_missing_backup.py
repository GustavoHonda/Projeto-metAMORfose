# Contadores por profissional
professional_counts = df_selected_matches['phone_professional'].value_counts().to_dict()

# Conjuntos de pacientes já atribuídos
all_assigned_patients = set(df_selected_matches['phone_paciente'])

# Todos os profissionais
prof_phones = set(df_professional['phone_professional'])

new_matches = []



print("🔹 Verificando pacientes faltantes")
for phone in prof_phones:
    count = professional_counts.get(phone, 0)
    needed = max_patients - count
    if needed <= 0:
        print(f"    ✅ Profissional {phone} já possui {count} pacientes.")
        continue
    
    # Todos os candidatos para este profissional
    possible_matches = df_all_matches[df_all_matches['phone_professional'] == phone].copy()
    
    # Regra 1: pacientes distintos não usados ainda
    new_candidates = possible_matches[~possible_matches['phone_paciente'].isin(all_assigned_patients)]
    sampled = pd.DataFrame()
    remaining_needed = needed
    
    if len(new_candidates) >= remaining_needed:
        sampled = new_candidates.sample(remaining_needed, replace=False)
        remaining_needed = 0
        print(f"    Profissional {phone}: adicionados {len(sampled)} pacientes novos distintos (Regra 1).")
    else:
        sampled = new_candidates.copy()
        remaining_needed -= len(new_candidates)
        print(f"    Profissional {phone}: apenas {len(new_candidates)} pacientes novos distintos disponíveis (Regra 1).⚠️")
    
    # Regra 2: repetir pacientes não atribuídos a outros profissionais
    if remaining_needed > 0:
        unassigned_patients = possible_matches[
            ~possible_matches['phone_paciente'].isin(df_selected_matches['phone_paciente'])
        ]
        if not unassigned_patients.empty:
            repeat_needed = min(remaining_needed, len(unassigned_patients))
            repeated = unassigned_patients.sample(repeat_needed, replace=False)
            sampled = pd.concat([sampled, repeated], ignore_index=True)
            remaining_needed -= len(repeated)
            print(f"    Profissional {phone}: adicionados {len(repeated)} pacientes repetidos não usados por outros (Regra 2).⚠️")
    
    # Regra 3: se ainda faltar, repetir qualquer paciente do próprio profissional
    if remaining_needed > 0:
        if not possible_matches.empty:
            repeated_any = possible_matches.sample(remaining_needed, replace=True)
            sampled = pd.concat([sampled, repeated_any], ignore_index=True)
            print(f"    Profissional {phone}: adicionados {len(repeated_any)} pacientes repetidos de qualquer tipo (Regra 3).‼️")
        else:
            print(f"    Profissional {phone}: nenhum paciente disponível para completar as {max_patients} vagas.‼️")
    
    if not sampled.empty:
        new_matches.append(sampled)
        professional_counts[phone] = count + len(sampled)
        all_assigned_patients.update(sampled['phone_paciente'])

# Concatena novos matches
if new_matches:
    df_extra_matches = pd.concat(new_matches, ignore_index=True)
    df_selected_matches = pd.concat([df_selected_matches, df_extra_matches], ignore_index=True)
    print(f"Resultado: ✅ Total de {len(df_extra_matches)} novos matches adicionados.")
else:
    print("Resultado: ✅ Nenhum novo match necessário.")

# Estado final
print("\n🔹 Estado final dos profissionais:")
for phone in prof_phones:
    final_count = df_selected_matches[df_selected_matches['phone_professional'] == phone].shape[0]
    print(f"    Profissional {phone}: {final_count} pacientes atribuídos")

# 
# 
# 


# Algoritmo guloso
    for _, row in df_selected_matches.iterrows():
        paciente = row['phone_paciente']
        professional = row['phone_professional']
        chave = (paciente, professional)

        if chave in matchings_existentes:
            continue
        if paciente_counts[paciente] >= 1:       # cada paciente só pega 1 profissional
            continue
        if professional_counts[professional] >= 4:  # cada profissional no máximo 4 pacientes
            continue

        # Adiciona o matching
        matchings_final.append(row)
        paciente_counts[paciente] += 1
        professional_counts[professional] += 1