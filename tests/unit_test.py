import unittest
from langchain_core.runnables import RunnableConfig
from src.patent_researcher_graph.nodes.create_high_level_domain_map import CreateHighLevelDomainResearchMap
from src.patent_researcher_graph.state import PatentResearchGraphState
from src.patent_researcher_graph.configuration import Configuration
from src.patent_researcher_graph.state import DomainRelationship

class TestDefineOverallResearchDomainReal(unittest.TestCase):
    def setUp(self):
        """Configura la instancia del nodo antes de cada prueba"""
        self.node = CreateHighLevelDomainResearchMap()

        # Simular un estado válido con TODAS las entradas inicializadas
        self.test_state = PatentResearchGraphState(
            company_name="EcoBattery Inc.",
            industry="Energy Storage & Battery Manufacturing",
            products_services="Advanced lithium-titanate battery electrodes",
            region="Asia, Europe",
            technology="Li-titanate electrode innovation, including advanced doping techniques",
            strategic_objectives=["Identify new processes", "Benchmark competitor technologies"],
            number_sub_fields=3,
            research_statement="""The research statement for EcoBattery Inc. is to comprehensively map the patent landscape of advanced lithium-titanate electrode technologies, with a focus on innovative doping techniques and manufacturing processes. This analysis aims to identify emerging opportunities and benchmark global competitors within the Energy Storage & Battery Manufacturing industry across Asia and Europe, aligning with EcoBattery Inc.'s strategic objectives to discover new processes and enhance competitive positioning.""",
            main_domains=[],  
            total_sub_fields=[],  
            prioritized_sub_fields=[],  
            research_plans=[],  
            list_docx_report_dir=[],  
            consolidated_docx_report_dir="",  
            messages=[]
        )

        # ✅ Asegurar que config es una instancia válida
        self.config = RunnableConfig(configurable=Configuration())

    """def test_research_statement_generation(self):
        output = self.node.run(self.test_state, self.config)

        # Verificar que la salida contiene "research_statement"
        self.assertIn("research_statement", output)
        self.assertTrue(len(output["research_statement"]) > 0, "El research_statement generado está vacío")

        print("\n✅ Generated Research Statement:\n", output["research_statement"])"""
        
    def test_high_level_domain_map_generation(self):
        output = self.node.run(self.test_state, self.config)
        self.assertIn("main_domains", output)
        main_domains = output["main_domains"]
        self.assertIsInstance(main_domains, list)
        self.assertGreater(len(main_domains), 0, "El mapa de dominios no debe estar vacío.")
        for domain in main_domains:
            self.assertIsInstance(domain, DomainRelationship)
            domain_dict = domain.model_dump()
            self.assertIn("domain", domain_dict, "Falta el atributo 'domain'")
            self.assertIn("elements", domain_dict, "Falta el atributo 'elements'")
            self.assertIn("relationship", domain_dict, "Falta el atributo 'relationship'")
        print("\n✅ Generated High-Level Domain Map:")
        for d in main_domains:
            print(d.model_dump())

if __name__ == "__main__":
    unittest.main()
