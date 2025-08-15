import sys
import os
import django
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pandas as pd

from ABIMAQ.models import PesquisaABIMAQ

os.environ.setdefault('DJANGO_SETTINGS_MODULE',  'meu_projeto.settings')
django.setup()

def run_spark_job(pesquisa_id):
    try:
        pesquisa = PesquisaABIMAQ.objects.get(id=pesquisa_id)
        spark = SparkSession.builder.appName(f'ETL_ABIMAQ_{pesquisa_id}')
        print(F'Sessão do Spark iniciado para a pesquisa {pesquisa_id}')

        pesquisa.status = 'carregando'
        pesquisa.save()

        
        data =  [(1, 'dado_A'), (2, 'dado_B'), (3,'dado_C')]
        df_dados = spark.createDataframe(data,["id","nome"])

        resultados_df = df_dados.filter(col("id") > 1)
        resultado_df_pandas = resultados_df.toPandas()

        caminho_final = f'./uploads/resultado_{pesquisa_id}.xlsx'
        with pd.ExcelWriter(caminho_final) as writer:
            resultado_df_pandas.toExcel(writer, sheet_name='Planilha1', index=False)

        
        pesquisa.status = 'sucesso'
        pesquisa.caminho_resultado = caminho_final
        pesquisa.save()
        print(f'`Processamento  da pesquisa {pesquisa_id} concluído com sucesso')

    except Exception as e:
        if 'Pesquisa' in locals():
            pesquisa.status = 'erro'
            pesquisa.save()
        print(f'Erro no processamento da pesquisa{pesquisa_id}')
        raise

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_spark_job(sys.argv[1])
    else:
        print("Erro, nenhum ID de pesquisa foi fornecido")
