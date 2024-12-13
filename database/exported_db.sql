--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6
-- Dumped by pg_dump version 16.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categoria_documento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categoria_documento (
    codigo_categoria integer NOT NULL,
    nombre_categoria text NOT NULL,
    ruta_categoria text NOT NULL
);


ALTER TABLE public.categoria_documento OWNER TO postgres;

--
-- Name: encabezado_migracion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.encabezado_migracion (
    id_migracion integer NOT NULL,
    ruta_carpeta_base text NOT NULL
);


ALTER TABLE public.encabezado_migracion OWNER TO postgres;

--
-- Name: imagenes_catalogo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.imagenes_catalogo (
    id_imagen integer NOT NULL,
    nombre_imagen text NOT NULL,
    categoria_id integer
);


ALTER TABLE public.imagenes_catalogo OWNER TO postgres;

--
-- Name: imagenes_catalogo_id_imagen_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.imagenes_catalogo_id_imagen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.imagenes_catalogo_id_imagen_seq OWNER TO postgres;

--
-- Name: imagenes_catalogo_id_imagen_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.imagenes_catalogo_id_imagen_seq OWNED BY public.imagenes_catalogo.id_imagen;


--
-- Name: migracion_propiedades_archivos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.migracion_propiedades_archivos (
    id_reg integer NOT NULL,
    id_migracion integer DEFAULT 1 NOT NULL,
    nombre_archivo text,
    extension_archivo text,
    peso_archivo numeric,
    fecha_creacion timestamp without time zone,
    ruta_archivo text,
    llave text,
    hash_archivo text
);


ALTER TABLE public.migracion_propiedades_archivos OWNER TO postgres;

--
-- Name: migracion_propiedades_archivos_id_reg_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.migracion_propiedades_archivos_id_reg_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.migracion_propiedades_archivos_id_reg_seq OWNER TO postgres;

--
-- Name: migracion_propiedades_archivos_id_reg_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.migracion_propiedades_archivos_id_reg_seq OWNED BY public.migracion_propiedades_archivos.id_reg;


--
-- Name: imagenes_catalogo id_imagen; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagenes_catalogo ALTER COLUMN id_imagen SET DEFAULT nextval('public.imagenes_catalogo_id_imagen_seq'::regclass);


--
-- Name: migracion_propiedades_archivos id_reg; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.migracion_propiedades_archivos ALTER COLUMN id_reg SET DEFAULT nextval('public.migracion_propiedades_archivos_id_reg_seq'::regclass);


--
-- Data for Name: categoria_documento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categoria_documento (codigo_categoria, nombre_categoria, ruta_categoria) FROM stdin;
1	CATEGORIA_UNO	/CATEGORIA_UNO/...
2	CATEGORIA_DOS	/CATEGORIA_DOS/...
3	CATEGORIA_TRES	/CATEGORIA_TRES/...
\.


--
-- Data for Name: encabezado_migracion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.encabezado_migracion (id_migracion, ruta_carpeta_base) FROM stdin;
1	/contenedor_padre/
\.


--
-- Data for Name: imagenes_catalogo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.imagenes_catalogo (id_imagen, nombre_imagen, categoria_id) FROM stdin;
\.


--
-- Data for Name: migracion_propiedades_archivos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.migracion_propiedades_archivos (id_reg, id_migracion, nombre_archivo, extension_archivo, peso_archivo, fecha_creacion, ruta_archivo, llave, hash_archivo) FROM stdin;
\.


--
-- Name: imagenes_catalogo_id_imagen_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.imagenes_catalogo_id_imagen_seq', 1, false);


--
-- Name: migracion_propiedades_archivos_id_reg_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.migracion_propiedades_archivos_id_reg_seq', 1, false);


--
-- Name: categoria_documento categoria_documento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria_documento
    ADD CONSTRAINT categoria_documento_pkey PRIMARY KEY (codigo_categoria);


--
-- Name: encabezado_migracion encabezado_migracion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.encabezado_migracion
    ADD CONSTRAINT encabezado_migracion_pkey PRIMARY KEY (id_migracion);


--
-- Name: imagenes_catalogo imagenes_catalogo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.imagenes_catalogo
    ADD CONSTRAINT imagenes_catalogo_pkey PRIMARY KEY (id_imagen);


--
-- Name: migracion_propiedades_archivos migracion_propiedades_archivos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.migracion_propiedades_archivos
    ADD CONSTRAINT migracion_propiedades_archivos_pkey PRIMARY KEY (id_reg);


--
-- Name: idx_migracion_nombre_archivo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_migracion_nombre_archivo ON public.migracion_propiedades_archivos USING btree (nombre_archivo);


--
-- PostgreSQL database dump complete
--

