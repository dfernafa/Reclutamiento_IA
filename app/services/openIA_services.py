import os
import json
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from app.services.MongoStorageService import MongoStorageService
from app.models.diagnosis_IA import diagnosis_IA


class OpenAIServices:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_completion(self,resumen:str):
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "Eres un experto en selección de personal de jazzplat Colombia para áreas comerciales de telecomunicaciones de Colombia."},
                    {"role": "user", "content": self.promt_text(resumen)}
                ]
            )
            return self.clean_contenido_ia(response.choices[0].message.content)
    
    def clean_contenido_ia(self, contenido_ia: str) -> diagnosis_IA:
        contenido_ia = contenido_ia.strip()
        if contenido_ia.startswith("```json"):
            contenido_ia = contenido_ia.removeprefix("```json").strip()
        if contenido_ia.endswith("```"):
            contenido_ia = contenido_ia.removesuffix("```").strip()
        
        resultado = json.loads(contenido_ia)
        return diagnosis_IA(
            resultado=resultado.get("evaluacion_general", ""),
            resultado_json=resultado
        )
    
    def promt_text(self,texto_hv :str):
        prompt = f"""
                Actúa como un reclutador experto en selección de personal especializado en telecomunicaciones, enfocado en perfiles comerciales Inbound y Outbound.

                🛑 Regla prioritaria:
                Si el candidato tiene experiencia en ventas, aunque sea temporal, considera que **cumple inicialmente** con el perfil. Evalúa el resto de condiciones para confirmar la viabilidad, pero esta experiencia lo hace pasar el primer filtro,(Open english) es un buen candidato para lo que busco.

                Tu tarea es analizar el siguiente currículum vitae y determinar si el candidato cumple con el perfil requerido, considerando tanto el cumplimiento estricto de los requisitos como su potencial para desarrollarse en el cargo.

                Sé riguroso en la evaluación, pero también identifica talentos que puedan adaptarse y aprender rápidamente. Considera experiencias previas similares, habilidades transferibles y actitudes compatibles con el rol.

                Ten en cuenta además las siguientes condiciones adicionales:
                - Verifica si el candidato tiene vacíos laborales prolongados entre trabajos o si tiene historial de inestabilidad (menos de 3 meses por empleo). Evalúa su constancia.
                - Toda experiencia en ventas o atención al cliente debe valorarse, especialmente si es en contextos comerciales.
                - Evalúa experiencia específica en ventas cruzadas, ventas en frío, ventas inbound y habilidades claras de venta.
                - Si el candidato menciona niveles de inglés B2 o C1 pero no los certifica, analiza el CV con mayor rigurosidad, ya que podría haber riesgo de fuga hacia campañas en inglés.
                - Experiencia previa en call centers se considera como punto positivo.
                - Experiencia en líneas de teleoperador relacionadas con telecomunicaciones es altamente valorada.
                - Si el candidato tiene estudios en Derecho o temas legales, debe ser automáticamente descartado del proceso (NO CUMPLE).

                Tu respuesta debe estar en formato JSON con la siguiente estructura:

                {{
                "evaluacion_general": "CUMPLE"| "NO CUMPLE",
                "nombre": "Nombre de la persona",
                "edad":"Edad",
                "telefono" : "Telefono si lo contiene",
                "Correo":"Correo si lo contiene",
                "motivo": "Breve explicación general del porqué de la evaluación, considerando fortalezas y debilidades.",
                "aspectos_cumplidos": [
                    "Lista de requisitos del perfil que se cumplen"
                ],
                "aspectos_no_cumplidos": [
                    "Lista de requisitos que no se cumplen"
                ],
                "informacion Faltante": [
                    "Lista de requisitos que hace falta y podría ser relevante para el cargo"
                ],
                "potencial_detectado": "Sí" | "No",
                "tipo_de_agente_sugerido": "Inbound" | "Outbound" | "Ambos" | "No aplica",
                "observaciones_adicionales": "Cualquier comentario adicional relevante para la toma de decisión, como sugerencias de capacitación u observaciones actitudinales.",
                "veredicto": "Llamar" | "No Llamar"
                }}

                ### Perfil requerido:
                -Edad: Mayor de edad.
                -Nacionalidad: Colombiano o extranjero con residencia permanente.
                -Género: Indiferente.
                -Reintegros: No aceptados.
                -Disponibilidad horaria: Entre 1:00 a.m. y 6:00 p.m.
                -Formación mínima: Bachiller. Si es estudiante, máximo 5° semestre universitario.
                -Experiencia previa (mínimo 5 meses recientes) en áreas comerciales de telecomunicaciones:
                    - Inbound (Jazztel, Masivo Móvil Orange, FideAten Yoigo): manejo de KPIs de atención al cliente (TMO, calidad, rellamada, encuesta) y de ventas (portabilidad, migraciones, línea nueva).
                    - Outbound (FideOut): experiencia en venta outbound, con KPIs de activación, efectividad y productividad.

                ----Habilidades requeridas:
                - Comunicación efectiva, orientación al cliente, creatividad.
                - Cierre de acuerdos, tolerancia a la presión, orientación a resultados.

                ----Exclusiones:
                - Nivel de inglés superior a A2 no es aceptado si está certificado. Si menciona B2 o C1 sin certificar, analizar con sospecha de fuga.
                - Estudios en Derecho o formación legal: descartar automáticamente.
                - Debe tener red de apoyo (entorno estable para trabajo con turnos rotativos).

                --Servicios a evaluar:
                Masivo móvil Orange / Fide Aten Yoigo / Atención Jazztel (Inbound):
                - Soporte técnico básico, facturación, aclaraciones de planes, coberturas, venta de servicios y retención.

                --Cumplimiento de procedimientos, métricas de plataforma, revisión de actualizaciones y correos, adherencia al turno.
                FideOut (Outbound):
                - Ventas en llamada, configuración de actos comerciales, cumplimiento de métricas, revisión de actualizaciones y adherencia.

                ### CV extraído:
                {texto_hv}
                """ 
        return prompt
    

