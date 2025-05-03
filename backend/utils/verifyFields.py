def verify(name, email, endereco, idade, cpf, interesses, eventos, atividades, compras, user_photo):
    errors = []

    if not name.strip():
        errors.append("O campo nome deve ser preenchido") 

    if not email.strip() or '@' not in email:
        errors.append("Por favor insira corretamente seu email de uso frequente")

    if not endereco.strip():
        errors.append("O endereço deve ser preenchido")

    if not idade.isdigit() or int(idade) < 5 or int(idade) > 100:
        errors.append("Digite uma idade válida")

    if not cpf.strip():
        if len(cpf) != 11:
            errors.append("O campo de CPF deve ter 11 dígitos") 
    
    if not interesses.strip():
        errors.append("Ö campo de interesses deve ser preenchido")

    if not eventos.strip():
        errors.append("O campo de eventos deve ser preenchido")

    if not atividades.strip():
        errors.append("O campo de atividades deve ser preenchido")

    if not compras.strip():
        errors.append("O campo de compras deve ser preennchido corretamente")

    if user_photo == None:
        errors.append("Insira uma foto válida")

    return errors