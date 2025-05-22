from mcp.server.fastmcp import FastMCP
from mcp.types import Resource



# GRAPHQL SCHEMA
graphql_schema = """
    type Comarca @node{
        cod:String!,
        nombre:String!,
        geometry:String!,
        municipios:[Municipio!]! @relationship(type: "EN_COMARCA", direction: IN)
    }
    # Municipio represents the municipality node in the graph.
    type Municipio @node {
        cod: String!,
        nombre: String,
        geometry: String,
        figura_plan: String,
        longitud_carreteras: Float,
        longitud_viario: Float,
        superficie: Float,
        superficie_no_urbanizable: Float,
        superficie_urbanizable: Float,
        superficie_urbano: Float,
        densidad_habitantes: Float,
        precio_medio_alquiler: Float,
        viviendas_totales: Int,
        # List of districts (Distrito) associated with the municipality
        distritos: [Distrito!]! @relationship(type: "MUNICIPIO", direction: IN),
        # List of expenses projected in the municipality budgets
        gastos: [Gasto!]! @relationship(type: "TIENE_PRESUPUESTO", direction: OUT),
        # List of initial forecast in the municipality budgets
        previsones: [Prevision!]! @relationship(type: "TIENE_PRESUPUESTO", direction: OUT),
        # List of initial credits in the municipality budgets
        creditos_iniciales: [Credito_inicial!]! @relationship(type: "TIENE_PRESUPUESTO", direction: OUT),
        # List of dangers zones for flooding in the municipality
        peligros_inundacion: [Peligro_Inundacion!]! @relationship(type: "RIESGO_DE", direction: OUT),
        # List of risks zones for flooding in the municipality
        riesgos_inundacion: [Riesgo_Inundacion!]! @relationship(type: "RIESGO_DE", direction: OUT)
        # List of streets (Calle) associated with the municipality
        calles: [Calle!]! @relationship(type: "MUNICIPIO", direction: IN)
        # List of evolution of rental prices in the municipality
        precios_alquiler: [Precio_Alquiler!]! @relationship(type: "TIENE_PRECIO_ALQUILER", direction: OUT)
        # List of meteorology predicition in the municipality
        prediciones_meteorologicas:[Tiempo!]! @relationship(type: "REGISTRA_METEOROLOGIA", direction:OUT)
        # List of active meteorology alerts active
        alertas_meteorologicas_activas:[Alerta_Meteorologica!]! @relationship(type:"TIENE_ALERTA_METEOROLOGICA_ACTIVA", direction: OUT)
        # List of future meteorology alerts
        alertas_meteorologicas_futuras:[Alerta_Meteorologica!]! @relationship(type:"TIENE_ALERTA_METEOROLOGICA_FUTURA",direction:OUT)
        # List of statistics of Criminality
        estadisticas_criminalidad:[Criminalidad!]! @relationship(type:"TIENE_ESTADISTICAS_CRIMINALIDAD",direction:OUT)
        # ayuntamiento de alicante
        ayuntamiento:Ayuntamiento @relationship(type:"ADMINISTRADO_POR", direction:OUT)
        # estadisticas de demografia
        estadisticas_demografia: [Demografia!]! @relationship(type: "DISTRIBUCION_SEXO_POBLACION", direction: OUT)
        # comarca that belongs the municipality
        comarca: Comarca @relationship(type: "EN_COMARCA", direction: OUT)
        # estadisticas de paro
        estadisticas_paro: [Paro!]! @relationship(type: "TIENE_ESTADISTICA", direction: OUT)
        # estadisiticas de demandantes de empleo
        estadisticas_demandantes: [Demandante!]! @relationship(type: "TIENE_ESTADISTICA", direction: OUT)
        # estadisticas de afiliacion
        estadisticas_afiliacion: [Afiliacion!]! @relationship(type: "TIENE_ESTADISTICA", direction: OUT)
        # estadisticas pensiones
        estadisticas_pensiones: [Pension!]! @relationship(type: "TIENE_ESTADISTICA", direction: OUT)
        # estadisticas contratos
        estadisticas_contratos: [Contrato!]! @relationship(type: "TIENE_ESTADISTICA",direction:OUT)
    }
    # Calle represents the street node in the graph.    
    type Calle @node {
        cod: Int!,
        dir_completa: String,
        nombre: String,
        tipo: String,
        inmuebles: [Inmueble!]! @relationship(type: "CALLE", direction: IN)
        municipio: Municipio @relationship(type: "MUNICIPIO", direction: OUT)
    }
    # Distrito represents the district node in the graph.   
    type Distrito @node {
        distrito: String!,
        precio_medio_alquiler: Float,
        geometry: String,
        # List of census sections (Seccion_Censal) associated with the district
        secciones_censales: [Seccion_Censal!]! @relationship(type: "PERTENECE", direction: IN)
        # List the establecimientos (Establecimiento) associated with the distrito
        distribucion_establecimientos: [TipoEstablecimiento]!
    }
    # Seccion_Censal represents the census section node in the graph.
    type Seccion_Censal @node {
        codigo_seccion: String!,
        precio_medio_alquiler: Float,
        geometry: String,
        seccion:String,
        # List of demographic statistics data (Demografia) associated with the census section
        demografias: [Demografia!]! @relationship(type: "ASOCIADO", direction: IN)
        # List of incomes statistics data (Renta) associated with the census section
        rentas: [Renta!]! @relationship(type: "ASOCIADO", direction: IN)
        # List of buildings (Inmueble) associated with the census section
        inmuebles: [Inmueble!]! @relationship(type: "PERTENECE", direction: IN)
        # List the establecimientos (Establecimiento) associated with the census section
        distribucion_establecimientos: [TipoEstablecimiento]!

    }
    # Poligono_Catastral_Rustico represents the rural cadastral polygon node in the graph.
    type Poligono_Catastral_Rustico @node {
        hoja: String,
        masa: String,
        geometry: String
        parcelas: [Parcela!]! @relationship(type: "SE_ENCUENTRA", direction: IN)
    }
    # Poligono_Catastral_Urbano represents the urban cadastral polygon node in the graph.
    type Poligono_Catastral_Urbano @node{
        masa: String,
        geometry: String,
        parcelas: [Parcela!]! @relationship(type: "SE_ENCUENTRA", direction: IN)
    }
    # Parcela represents the parcel node in the graph.
    type Parcela @node {
        pcat1: String,
        pcat2: String,
        refcat: String,
        masa: String,
        poligono_catastral_rustico: [Poligono_Catastral_Rustico!]! @relationship(type: "SE_ENCUENTRA", direction: OUT),
        poligono_catastral_urbano: [Poligono_Catastral_Urbano!]! @relationship(type: "SE_ENCUENTRA", direction: OUT)
        inmuebles: [Inmueble!]! @relationship(type: "PERTENECE", direction: IN)
    }

    type Alquiler @node{
        simulacion_gobierno_max: Float,
        simulacion_gobierno_min: Float,
        simulacion_metodo_1: Float,
        simulacion_metodo_2: Float,
        simulacion_metodo_3: Float
    }

    # Inmueble represents the property node in the graph.
    type Inmueble @node{
        refcat:String!,
        direccion:String,
        clase:String,
        geometry:String,
        superficie:Float,
        uso_principal:String,
        simulacion_alquiler: [Alquiler!]! @relationship(type:"SIMULACION",direction:OUT),
        # point that represents the location of the property or of the parcel that belongs
        punto: Point,
        anyo_construccion:Int @alias(property: "año_construcción"),
        # List of elements (Construccion) associated with that property
        construcciones: [Construccion!]! @relationship(type: "PERTENECE", direction: IN),
        calle: Calle @relationship(type: "CALLE", direction: OUT),
    }

    type Construccion @node{
        escalera:Int,
        planta:Int,
        puerta:Int,
        superficie:Float,
        tipo_reforma:String,
        uso:String
    }

    type Distribucion_Sexo @relationshipProperties{
        hombres:Int,
        mujeres:Int
    }

    type Distribucion_Pais_Nacimiento @relationshipProperties{
        extranjeros:Int,
        espanoles:Int @alias(property:"españoles")
    }

    type Grupo_Edad @node{
        rango:String
    }
    
    type Pais @node{
        nombre:String,
        geometry:String
        continente: Continente @relationship(type: "CONTINENTE", direction: OUT)
    }

    type Continente @node{
        nombre:String,
        geometry:String,
    }

    type Demografia @node{
        edad_media_de_la_poblacion: Int @alias(property:"Edad_media_de_la_población"),
        anyo: Int @alias(property:"año"),
        poblacion: Int @alias(property:"población"),
        porcentaje_de_hogares_unipersonales: Float,        
        porcentaje_de_poblacion_de_65_y_mas_anyos: Int @alias(property:"porcentaje_de_población_de_65_y_más_años"),
        porcentaje_de_poblacion_espanola: Int @alias(property:"porcentaje_de_población_española"),
        porcentaje_de_poblacion_menor_de_18_anyos: Int @alias(property:"porcentaje_de_población_menor_de_18_años"),
        porcentaje_poblacion_entre_18_y_64_anyos: Int @alias(property:"porcentaje_poblacion_entre_18_y_64_años"),
        porcentaje_poblacion_extranjera:Int @alias(property:"porcentaje_poblacion_extranjera"), 
        tamanyo_medio_del_hogar: Float @alias(property:"tamaño_medio_del_hogar"),
        # List of age groups (Grupo_Edad) distribution associated with the demographic statistics
        rangos_edad: [Grupo_Edad!]! @relationship(type: "DISTRIBUCION_SEXO",properties:"Distribucion_Sexo", direction: OUT), 
        # List of nationalities (Pais) distribution associated with the demographic statistics
        nacionalidades: [Pais!]! @relationship(type: "DISTRIBUCION_SEXO_NACIONALIDAD",properties:"Distribucion_Sexo", direction: OUT)
        # List of birth countries (Pais) distribution associated with the demographic statistics
        paises_nacimiento: [Pais!]! @relationship(type: "DISTRIBUCION_SEXO_PAIS_NACIMIENTO",properties:"Distribucion_Sexo", direction: OUT)
        # List of occupations (Ocupacion) distribution associated with the demographic statistics
        ocupaciones: [Ocupacion!]! @relationship(type: "DISTRIBUCION_SEXO", properties:"Distribucion_Sexo", direction: OUT)
        # List of education levels stats by sex (Nivel_Estudio) distribution associated with the demographic statistics
        nivel_estudios_por_sexo: [Nivel_Estudio!]! @relationship(type: "DISTRIBUCION_SEXO", properties:"Distribucion_Sexo", direction: OUT)  
        # List of education levels stats by birth country (Nivel_Estudio) distribution associated with the demographic statistics
        nivel_estudios_por_pais_nacimiento: [Nivel_Estudio!]! @relationship(type: "DISTRIBUCION_PAIS_NACIMIENTO", properties:"Distribucion_Pais_Nacimiento", direction: OUT)
        # List of economic activities stats [Actividad_Economica] distribution associated with the demographic statistics
        actividad_economicas: [Actividad_Economica!]! @relationship(type: "DISTRIBUCION_SEXO", properties:"Distribucion_Sexo", direction: OUT),
        # List of professional situations stats [Situacion_Profesional] distribution associated with the demographic statistics
        situaciones_profesionales: [Situacion_Profesional!]! @relationship(type: "DISTRIBUCION_SEXO", properties:"Distribucion_Sexo", direction: OUT),
        # List of activities stats by sex [Actividad] distribution associated with the demographic statistics
        actividad_por_sexo: [Actividad!]! @relationship(type: "DISTRIBUCION_SEXO", properties:"Distribucion_Sexo", direction: OUT)
        # List of activities stats by birth country [Actividad] distribution associated with the demographic statistics
        actividad_por_pais_nacimiento: [Actividad!]! @relationship(type: "DISTRIBUCION_PAIS_NACIMIENTO", properties:"Distribucion_Pais_Nacimiento", direction: OUT)
    }

    type Renta @node{
        distribucion_de_la_renta_P80_P20: Float @alias(property:"Distribución_de_la_renta_P80_P20"),
        anyo: Int @alias(property:"año"),
        fuente_ingreso_otras_prestaciones: Float,
        fuente_ingreso_otros: Float,
        fuente_ingreso_pension: Float,
        fuente_ingreso_prestaciones_desempleo: Float,
        fuente_ingreso_salario: Float,
        renta_media_bruta_por_persona: Float,
        indice_de_gini: Float @alias(property:"Índice_de_Gini"),
        secciones_censales: [Seccion_Censal!]! @relationship(type: "ASOCIADO", direction: OUT)
    }

    type Demografia @node{
        anyo:Int @alias(property:"año"),
        indice_de_envejecimiento:Float,
        indice_de_longevidad:Float,
        indice_de_maternidad:Float,
        indice_de_renovacion_poblacion_activa:Float,
        indice_de_tendencia:Float,
        muertes:Int,
        nacimientos:Int,
        poblacion:Int @alias(property:"población"),
        tasa_de_dependencia:Float,
        tasa_de_dependencia_de_la_poblacion_mayor_64_anyos:Float,
        tasa_de_dependencia_de_la_poblacion_menor_16_anyos:Float
        distribucion_sexo_poblacion: [Municipio!]! @relationship(type: "DISTRIBUCION_SEXO_POBLACION", properties: "Distribucion_Sexo", direction: IN)
        distribucion_sexo_natalidad: [Municipio!]! @relationship(type: "DISTRIBUCION_SEXO_NATALIDAD", properties: "Distribucion_Sexo", direction: IN)
        distribucion_sexo_mortalidad: [Municipio!]! @relationship(type: "DISTRIBUCION_SEXO_MORTALIDAD", properties: "Distribucion_Sexo", direction: IN)
    }

    interface Mobiliario{
        point: Point
    }

    type Luminaria @node{
        tipo:String,
        potencia_w:String,
        point: Point
    }

    type Basura @node{
        num_matricula: String,
        tipo: String,
        matricula: String @alias(property:"matrícula"),
        point:Point}

    
    type Gasto @node{
        actuaciones_de_caracter_economico: Float @alias(property:"actuaciones_de_carácter_económico"),
        actuaciones_de_caracter_general: Float @alias(property: "actuaciones_de_carácter_general"),
        actuaciones_de_proteccion_y_promocion_social: Float @alias(property: "actuaciones_de_protección_y_promoción_social"),
        anyo: Int @alias(property: "año"),
        deuda_publica: Float @alias(property: "deuda_pública"),
        produccion_de_bienes_publicos_de_caracter_preferente: Float @alias(property: "producción_de_bienes_públicos_de_carácter_preferente"),
        servicios_publicos_basicos: Float @alias(property: "servicios_públicos_básicos"),
        total_gastos: Float
    }

    type Prevision @node(labels: ["Previsión"]){
        activos_financieros:Float,
        anyo: Int @alias(property: "año"),
        enajenacion_inversiones_reales: Float @alias(property: "enajenación_inversiones_reales"),
        impuestos_directos: Float,
        impuestos_indirectos: Float,
        ingresos_patrimoniales: Float,
        pasivos_financieros: Float,
        tasas_y_otros_ingresos: Float,
        total_ingresos: Float,
        transferencias_corrientes: Float,
        transferencias_de_capital: Float
    }
    
    type Credito_inicial @node(labels: ["Crédito_inicial"]){
        activos_financieros:Float,
        anyo: Int @alias(property: "año"),
        fondo_de_contingencia: Float,
        gastos_de_personal: Float,
        gastos_en_bienes_ctes_y_servicios: Float,
        gastos_financieros: Float,
        inversiones_reales: Float,
        pasivos_financieros: Float,
        total_gastos_creditos: Float @alias(property: "total_gastos_créditos"),
        transferencias_corrientes: Float,
        transferencias_de_capital: Float
    }

    type Ocupacion {
        ocupacion: String,
    }

    type Nivel_Estudio{
        nivel : String
    }

    type Actividad_Economica{
        actividad: String
    }

    type Situacion_Profesional{
        situacion_profesional: String
    }

    type Actividad @node{
        actividad: String
    }


    type Peligro_Inundacion @node(labels: ["Peligro"]){
        demarcacion: String,
        descripcion_peligro: String,
        fuente: String,
        geometry: String,
        nivel_peligro: Int,
        retorno: Int
    }

    type Riesgo_Inundacion @node(labels: ["Riesgo"]){
        riesgo: String,
        fuente: String,
        geometry: String,
    }

    type Precio_Alquiler @node{
        anyo: Int @alias(property:"año"),
        mes: String,
        precio_m2_Fotocasa: String,
        precio_m2_Idealista: String,
        precio_m2_Indomio: String,
    }

    type Establecimiento {
        nombre:String,
        punto: Point
    }

    type TipoEstablecimiento{
        tipo:String,
        numero_establecimientos: Int!
        establecimientos: [Establecimiento!]!
    }

    type Tiempo{
        estadoCielo:String, 	
        fecha:DateTime, 	
        humedadRelativa_maxima:Int,
        humedadRelativa_minima:Int,
        precipitacion:Int,
        sensacionTermica_maxima:Int,
        sensacionTermica_minima:Int,
        temperatura_maxima:Int,
        temperatura_minima:Int,
        viento_direccion:String,
        viento_velocidad:Int,
        probabilidad_precipitacion_por_horas:Probabilidad_Precipitacion @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        cota_nieve_por_horas:Cota_Nieve @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        estado_cielo_por_horas:Estado_Cielo @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        viento_por_horas:Viento @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        racha_maxima_viento_por_horas:Racha_Maxima_Viento @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        temperatura_por_horas:Temperatura @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        sensacion_termica_por_horas:Sensacion_Termica @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT),
        humedad_relativa_por_horas:Humedad_Relativa @relationship(type:"REGISTRA_METEOROLOGIA_ESPECIFICA",direction:OUT)
    }

    type Probabilidad_Precipitacion{
        doce_am__seis_am:Int @alias(property: "00-06"),
        seis_am__doce_pm:Int @alias(property: "06-12"),
        doce_pm__seis_pm:Int @alias(property: "12-18"),
        seis_pm__doce_am:Int @alias(property: "18-24")
    }

    type Cota_Nieve{
        doce_am__seis_am:String @alias(property: "00-06"),
        seis_am__doce_pm:String @alias(property: "06-12"),
        doce_pm__seis_pm:String @alias(property: "12-18"),
        seis_pm__doce_am:String @alias(property: "18-24")
    }

    type Estado_Cielo{
        doce_am__seis_am:String @alias(property: "00-06"),
        seis_am__doce_pm:String @alias(property: "06-12"),
        doce_pm__seis_pm:String @alias(property: "12-18"),
        seis_pm__doce_am:String @alias(property: "18-24")
    }
    
    type Viento{
        doce_am__seis_am:String @alias(property: "00-06"),	
        seis_am__doce_pm:String @alias(property: "06-12"),	
        doce_pm__seis_pm:String @alias(property: "12-18"),	
        seis_pm__doce_am:String @alias(property: "18-24")	
    }


    type Racha_Maxima_Viento{
        doce_am__seis_am:String @alias(property: "00-06"),	
        seis_am__doce_pm:String @alias(property: "06-12"),	
        doce_pm__seis_pm:String @alias(property: "12-18"),	
        seis_pm__doce_am:String @alias(property: "18-24")	
    }

    type Temperatura{
        doce_am__seis_am:Int @alias(property: "00-06"),
        seis_am__doce_pm:Int @alias(property: "06-12"),
        doce_pm__seis_pm:Int @alias(property: "12-18"),
        seis_pm__doce_am:Int @alias(property: "18-24")
    }

    type Sensacion_Termica{
        doce_am__seis_am:Int @alias(property: "00-06"),
        seis_am__doce_pm:Int @alias(property: "06-12"),
        doce_pm__seis_pm:Int @alias(property: "12-18"),
        seis_pm__doce_am:Int @alias(property: "18-24")
    }

    type Humedad_Relativa{
        doce_am__seis_am:Int @alias(property: "00-06"),
        seis_am__doce_pm:Int @alias(property: "06-12"),
        doce_pm__seis_pm:Int @alias(property: "12-18"),
        seis_pm__doce_am:Int @alias(property: "18-24")
    
    }

    type Sensor{
        id_conf:String!,
        nombre:String!,
        tipo: String!,
        point:Point!,
        url: String,
        confederacion_hidografica: Confederacion_hidrografica @relationship(type: "GESTIONADO_POR", direction: OUT),
        mediciones:[Medicion!]! @relationship(type: "REGISTRA", direction:OUT),
        municipio: Municipio! @relationship(type:"EN_MUNICIPIO", direction:OUT)
    }


    type Confederacion_hidrografica @node(labels: ["Confederacion_Hidografica"]){
        id:String!,
        nombre:String!,
        area:String!,
        url:String!,
        geometry:String!,
        sensores:[Sensor!]! @relationship(type: "GESTIONADO_POR", direction: IN)
        
    }


    type Medicion{
        dia: Date,
        doce_am:String @alias(property:"00:00"),
        una_am:String @alias(property:"01:00"),
        dos_am:String @alias(property:"02:00"),
        tres_am:String @alias(property:"03:00"),
        cuatro_am:String @alias(property:"04:00"),
        cinco_am:String @alias(property:"05:00"),
        seis_am:String @alias(property:"06:00"),
        siete_am:String @alias(property:"07:00"),
        ocho_am:String @alias(property:"08:00"),
        nueve_am:String @alias(property:"09:00"),
        diez_am:String @alias(property:"10:00"),
        once_am:String @alias(property:"11:00"),
        doce_pm:String @alias(property:"12:00"),
        una_pm:String @alias(property:"13:00"),
        dos_pm:String @alias(property:"14:00"),
        tres_pm:String @alias(property:"15:00"),
        cuatro_pm:String @alias(property:"16:00"),
        cinco_pm:String @alias(property:"17:00"),
        seis_pm:String @alias(property:"18:00"),
        siete_pm:String @alias(property:"19:00"),
        ocho_pm:String @alias(property:"20:00"),
        nueve_pm:String @alias(property:"21:00"),
        diez_pm:String @alias(property:"22:00"),
        once_pm:String @alias(property:"23:00"),
        nivel_medio:String @alias(property:"NivelMedio"),
        volumen_diario:String @alias(property: "Volumdiario")    
    }

    type Alerta_Meteorologica{
        title:String,
        description:String,
        link:String,
        guid:String,
        pubDate:DateTime,
        urgency:String,
        severity:String,
        certainty:String,
        effective:DateTime,
        onset:DateTime,
        expires:DateTime,
        instruction:String,
        nivel_alerta:String,
        alerta_parametro:String,
        alerta_probabilidad:String,
        geometry:String,
        risk_type:String
    }


    type Criminalidad @node(labels: ["Criminalidad"]){
        anyo:Int @alias(property: "año"),
        cibercriminalidad:Int @alias(property: "cibercliminalidad"),
        criminalidad_ciber_especifica: Criminalidad_Ciber @relationship(type: "CRIMINALIDAD_CIBERDELINUCENCIA", direction: OUT)
        criminalidad_convencional:Int,
        criminalidad_convencional_especifica:Criminalidad_Convencional @relationship(type: "CRIMINALIDAD_CONVENCIONAL", direction: OUT)
        trimestre:Int
    }

    type Criminalidad_Convencional @node(labels:["Criminalidad","Convencional"]){
        anyo:Int @alias(property:"año"),
        delitos_contra_libertad_sexual:Int,
        desglose_delitos_sexual:Criminalidad_Convencional_Sexual @relationship(type: "CRIMINALIDAD_CONVENCIONAL_SEXUAL", direction: OUT)
        delitos_graves_menos_graves_lesiones_rinya_tumultuaria: Int @alias(property:"delitos_graves_menos_graves_lesiones_riña_tumultuaria"),
        homicidios_dolosos_asesinatos_consumados:Int,
        homicidios_dolosos_asesinatos_tentativa:Int,
        hurtos:Int,
        resto_criminalidad_convencional:Int,
        robos_fuerza_domicilios_establecimientos:Int,
        robos_violencia_intimidacion:Int,
        desglose_delitos_robos:Criminalidad_Convencional_Robos @relationship(type: "CRIMINALIDAD_CONVENCIONAL_ROBOS", direction: OUT)
        secuestro:Int,
        sustracciones_vehiculos:Int,
        trafico_drogas:Int,
        trimestre:Int
    }

    type Criminalidad_Convencional_Robos @node(labels: ["Criminalidad", "Robos"]){
        anyo:Int @alias(property:"año"),
        robos_fuerza_domicilios:Int,
        robos_fuerza_otros_estableciminetos_instalaciones:Int
        trimestre:Int
    }

    type Criminalidad_Ciber @node(labels:["Criminalidad","Ciberdelincuencia"]){
        anyo:Int @alias(property:"año"),
        estafas_informaticas:Int,
        otros_ciberdelitos:Int,
        trimestre:Int
    }

    type Criminalidad_Convencional_Sexual @node(labels:["Criminalidad","Sexual"]){
        anyo:Int @alias(property:"año"),
        agresion_sexual_con_penetracion: Int,
        resto_delitos_contra_libertad_sexual: Int,
        trimestre: Int
    }

    type Ayuntamiento{
        direccion:String,
        email:String,
        telefono:String,
        web:String,
        calle:Calle @relationship(type: "SITUADO_EN", direction: OUT)
    }

    type Tiene_estadistica_paro @relationshipProperties{
        total_parados:Int,
        censurado:Boolean
    }

    type Paro @node(labels: ["Paro","Empleo"]){
        anyo:Int @alias(property:"año"),
        mes:Int,
        total_parados:Int,
        censurado:Boolean,
        distribucion_por_grupo_edad:[Grupo_Edad!]! @relationship(type: "DISTRIBUCION_SEXO",properties:"Distribucion_Sexo", direction: OUT) 
        distribucion_por_actividad_economica:[Actividad_Economica!]! @relationship(type: "TIENE_ESTADISTICA",properties:"Tiene_estadistica_paro", direction: OUT)
    }

    type Tiene_estadistica_demandante @relationshipProperties{
        total_demandantes:Int,
        censurado:Boolean
    }

    type Demandante @node(labels: ["Empleo","Demandante"]){
        anyo:Int @alias(property:"año"),
        mes:Int,
        total_demandantes:Int,
        censurado:Boolean,
        distribucion_por_grupo_edad:[Grupo_Edad!]! @relationship(type: "DISTRIBUCION_SEXO",properties:"Distribucion_Sexo", direction: OUT)
        distribucion_por_actividad_economica:[Actividad_Economica!]! @relationship(type: "TIENE_ESTADISTICA",properties:"Tiene_estadistica_demandante", direction: OUT)
    }

    type Regimen_Afiliacion @node{
        regimen:String
    }

    type Afiliacion @node(labels: ["Empleo","Afiliacion"]){
        anyo:Int @alias(property:"año"),
        mes:Int,
        total_afiliados:Int @alias(property:"afiliados"),
        censurado:Boolean,
        distribucion_por_regimen_afiliacion:[Regimen_Afiliacion!]! @relationship(type: "DISTRIBUCION_SEXO",properties:"Distribucion_Sexo", direction: OUT)
    }

    type Pension @node{
        anyo:Int @alias(property:"año"),
        importe_mensual:Float,
        pension_media_mensual:Float,
        pensionistas:Int,
        trimestre:Int
    }

    type Tipo_Contrato @node{
        tipo:String
    }

    type Tiene_estadistica_contrato @relationshipProperties{
        total_contratos:Int,
        censurado:Boolean
    }

    type Contrato @node{
        anyo:Int @alias(property:"año"),
        mes:Int,
        total_contratos:Int,
        censuado:Boolean,
        distribucion_por_actividad_economica:[Actividad_Economica!]! @relationship(type: "TIENE_ESTADISTICA",properties:"Tiene_estadistica_contrato", direction: OUT)
        distribucion_por_tipo_contrato:[Tipo_Contrato!]! @relationship(type: "DISTRIBUCION_SEXO",properties:"Distribucion_Sexo", direction: OUT) 
    }
"""

mcp = FastMCP(
    name="GEOIA API Server",
    host="localhost",
    port=9999,
    sse_path="/sse"
)


@mcp.resource(
        uri="http://localhost:9999/sse/schema",
        name="GEOIA API GraphQL Schema",
        description="GraphQL schema for the GEOIA API",
        mime_type="text/plain",
)
def get_graphql_schema() -> str:
    """
    Provides the full GraphQL schema as context for downstream tools.
    """
    return graphql_schema


@mcp.tool()
def execute_graphql_query(grapqhl_query:str) -> str:
    """
    Executes a given GraphQL query.

    Parameters:
        grapqhl_query (str): The GraphQL query to be executed.
    """

    return grapqhl_query

if __name__ == '__main__':
    mcp.run(transport="sse")