import React, { useState, useEffect, useContext } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { apiUrl } from '../config/api';

const CompraIngresso = () => {
  const { sessaoId } = useParams(); // Pega o ID da sessão da URL
  const { token } = useContext(AuthContext); // Pega o token de login
  const navigate = useNavigate();

  const [dadosSessao, setDadosSessao] = useState(null);
  const [assentosOcupados, setAssentosOcupados] = useState([]);
  const [assentoSelecionado, setAssentoSelecionado] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mensagem, setMensagem] = useState('');

  const alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  useEffect(() => {
    // Se o usuário não estiver logado, manda pro Login
    if (!token) {
      navigate('/login');
      return;
    }

    const buscarDados = async () => {
      try {
        // 1. Busca os detalhes da sessão (para saber o tamanho da sala)
        const respSessao = await fetch(apiUrl(`/api/sessoes/${sessaoId}/`));
        const dadosSessao = await respSessao.json();
        setDadosSessao(dadosSessao);

        // 2. Busca a lista de assentos ocupados
        const respOcupados = await fetch(apiUrl(`/api/sessoes/${sessaoId}/assentos_ocupados/`));
        const dadosOcupados = await respOcupados.json();
        // Baseado no seu Postman, a API retorna um objeto com 'assentos_ocupados' dentro
        setAssentosOcupados(dadosOcupados.assentos_ocupados || []);

      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        setMensagem('Erro ao carregar o mapa da sala.');
      } finally {
        setLoading(false);
      }
    };

    buscarDados();
  }, [sessaoId, token, navigate]);

  // Função auxiliar para verificar se a cadeira está vendida
  const isOcupado = (fileira, coluna) => {
    return assentosOcupados.some(
      (assento) => assento.fileira === fileira && assento.coluna === coluna
    );
  };

  const confirmarCompra = async () => {
    if (!assentoSelecionado) return;
    setMensagem('Processando...');

    try {
      const response = await fetch(apiUrl('/api/reservas/'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Envia o token JWT
        },
        body: JSON.stringify({
          sessao: sessaoId,
          fileira: assentoSelecionado.fileira,
          coluna: assentoSelecionado.coluna
        })
      });

      if (response.ok) {
        setMensagem('Ingresso comprado com sucesso!');
        // Atualiza a lista visualmente adicionando o que acabamos de comprar
        setAssentosOcupados([...assentosOcupados, assentoSelecionado]);
        setAssentoSelecionado(null);
      } else {
        const erroData = await response.json();
        // Tenta pegar a mensagem de erro da API (como 'non_field_errors' do Django)
        setMensagem(`Erro: ${erroData.non_field_errors?.[0] || 'Cadeira já ocupada'}`);
      }
    } catch (error) {
      setMensagem('Erro de conexão com o servidor.');
    }
  };

  if (loading) return <p style={{ padding: '20px' }}>Carregando mapa da sala...</p>;
  if (!dadosSessao) return <p style={{ padding: '20px' }}>Sessão não encontrada.</p>;

  // Formata a data para exibir na tela
  const dataHoraFormatada = new Date(dadosSessao.horario_inicio).toLocaleString('pt-BR');

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto', textAlign: 'center' }}>
      <h2>{dadosSessao.filme_titulo}</h2>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        Sala: <strong>{dadosSessao.sala_nome}</strong> | Horário: <strong>{dataHoraFormatada}</strong>
      </p>

      {/* Representação visual da Tela do Cinema */}
      <div style={{ background: '#ccc', height: '15px', width: '60%', margin: '0 auto 40px auto', borderRadius: '4px' }}>
        TELA
      </div>

      {/* Grid de Assentos */}
      <div style={{ display: 'inline-block', padding: '10px', background: '#f5f5f5', borderRadius: '8px' }}>
        {Array.from({ length: dadosSessao.sala_fileiras }).map((_, indiceFileira) => {
          const letraFileira = alfabeto[indiceFileira];

          return (
            <div key={letraFileira} style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
              {/* Letra da Fileira */}
              <span style={{ width: '30px', fontWeight: 'bold', marginRight: '10px' }}>{letraFileira}</span>
              
              {/* Botões das Cadeiras */}
              {Array.from({ length: dadosSessao.sala_colunas }).map((_, indiceColuna) => {
                const numeroColuna = indiceColuna + 1;
                const ocupado = isOcupado(letraFileira, numeroColuna);
                const selecionado = assentoSelecionado?.fileira === letraFileira && assentoSelecionado?.coluna === numeroColuna;

                let corFundo = '#4CAF50'; // Livre (Verde)
                if (ocupado) corFundo = '#F44336'; // Ocupado (Vermelho)
                if (selecionado) corFundo = '#2196F3'; // Selecionado (Azul)

                return (
                  <button
                    key={`${letraFileira}-${numeroColuna}`}
                    onClick={() => setAssentoSelecionado({ fileira: letraFileira, coluna: numeroColuna })}
                    disabled={ocupado}
                    style={{
                      width: '35px',
                      height: '35px',
                      margin: '0 4px',
                      backgroundColor: corFundo,
                      color: 'white',
                      border: 'none',
                      borderRadius: '5px',
                      cursor: ocupado ? 'not-allowed' : 'pointer',
                      fontSize: '12px'
                    }}
                  >
                    {numeroColuna}
                  </button>
                );
              })}
            </div>
          );
        })}
      </div>

      {/* Painel de Ação (Abaixo do Mapa) */}
      <div style={{ marginTop: '30px', borderTop: '1px solid #eee', paddingTop: '20px' }}>
        {assentoSelecionado ? (
          <p style={{ fontSize: '1.2rem' }}>
            Assento escolhido: <strong>{assentoSelecionado.fileira}{assentoSelecionado.coluna}</strong>
          </p>
        ) : (
          <p style={{ color: '#666' }}>Selecione um assento verde no mapa acima.</p>
        )}
        
        <button 
          onClick={confirmarCompra} 
          disabled={!assentoSelecionado}
          style={{ 
            padding: '12px 24px', 
            fontSize: '16px', 
            background: !assentoSelecionado ? '#ccc' : '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: !assentoSelecionado ? 'not-allowed' : 'pointer' 
          }}
        >
          Confirmar Compra do Ingresso
        </button>

        {mensagem && <p style={{ marginTop: '15px', fontWeight: 'bold', color: mensagem.startsWith('Erro') ? 'red' : 'black' }}>{mensagem}</p>}
      </div>
    </div>
  );
};

export default CompraIngresso;