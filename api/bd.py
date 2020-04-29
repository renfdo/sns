from sns_flow.mysql_db.MysqlDAO import MysqlDAO

def sns_to_sql(dt):
    cols = {
        'Cod Unidade': 'cod_fab',
        'NomeUnidade': 'nom_abr_unb',
        'Cod Unidade Orig': 'cod_cliente',
        'Regional': 'dsc_regional',
        'Cod Cliente': 'cod_cliente_orig',
        'Nome Cliente': 'nom_fantasia_cliente',
        'Geografia': 'dsc_geo',
        'Categoria': 'liquido',
        'Emb. Aberta': 'embalagem_aberta',
        'Emb. Fechada': 'embalagem_fechada',
        'CodProduto': 'cod_produto',
        'Nome Prod': 'nom_abrev_prod',
        'Data Puxada': 'dat_original',
        'Marcacao': 'marcacao',
        'NS GROSS': 'ns_gross',
        'Status Item': 'sgl_status_item',
        'Motivo': 'dsc_motivo',
        'Numero Carro': 'num_carro',
        'Cod Justificativa': 'cod_justificativa',
        'Justificativa': 'dsc_justificativa',
        'Cod Justificativa BO': 'cod_justificativa_bo',
        'Justificativa BO': 'dsc_justificativa_bo',
        'Canal Marcacao': 'canal',
        'Entrada': 'entrada',
    }

    dt = dt.loc[:, list(cols.keys())].rename(columns=cols)
    dt['business_key'] = (
                            dt['dat_original'].astype('str')+'-' +
                            dt['cod_cliente'].astype('str')+'-' +
                            dt['cod_produto'].astype('str')+'-' +
                            dt['canal'].astype('str')+'-'
                        )

    engine = MysqlDAO.create_engine()
    # salva em uma tabela temporária
    dt.to_sql('temp_saidasns', con=engine, if_exists='replace', index=False)
    engine.dispose()

    # # deleta os registros que já existem
    sql_old_data = "SET SQL_SAFE_UPDATES = 0; DELETE SNS_SAIDASNS FROM SNS_SAIDASNS INNER JOIN temp_saidasns ON SNS_SAIDASNS.BUSINESS_KEY = temp_saidasns.BUSINESS_KEY;"

    columns = ",".join(list(cols.values()))
    sql_new_data = f"INSERT INTO sns_saidasns ({columns}) \
                     SELECT {columns} FROM temp_saidasns;"

    with engine.begin() as conn:  # TRANSACTION
        conn.execute(sql_old_data)
        conn.execute(sql_new_data)

