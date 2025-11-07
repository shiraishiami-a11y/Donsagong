// GoldenPeppaLoading.tsx - Golden Peppaローディングアニメーション
import { Box, Typography, keyframes } from '@mui/material';

// アニメーション定義
const gentleShake = keyframes`
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  25% {
    transform: rotate(-8deg) scale(1.02);
  }
  50% {
    transform: rotate(0deg) scale(1);
  }
  75% {
    transform: rotate(8deg) scale(1.02);
  }
`;

const rayGlowPart = keyframes`
  0%, 100% {
    opacity: 0.5;
    transform: scale(0.9);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
`;

const sparkleFall = keyframes`
  0% {
    top: calc(60% + 30px);
    left: calc(50% + 60px);
    transform: translateX(-50%) translateY(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    transform: translateX(-50%) translateY(40px) rotate(180deg);
    opacity: 1;
  }
  100% {
    top: calc(60% + 30px);
    left: calc(50% + 60px);
    transform: translateX(-50%) translateY(80px) rotate(360deg);
    opacity: 0;
  }
`;

const sparkleFallRight = keyframes`
  0% {
    top: calc(60% + 30px);
    left: calc(50% + 70px);
    transform: translateX(-50%) translateY(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    transform: translateX(-50%) translateY(40px) rotate(180deg);
    opacity: 1;
  }
  100% {
    top: calc(60% + 30px);
    left: calc(50% + 70px);
    transform: translateX(-50%) translateY(80px) rotate(360deg);
    opacity: 0;
  }
`;

const fallParticle = keyframes`
  0% {
    top: 0;
    opacity: 0;
    transform: translateX(0);
  }
  10% {
    opacity: 0.8;
  }
  50% {
    transform: translateX(-5px);
  }
  90% {
    opacity: 0.8;
    transform: translateX(5px);
  }
  100% {
    top: 100%;
    opacity: 0;
    transform: translateX(0);
  }
`;

const fadeInUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const dotPulse = keyframes`
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.3);
    opacity: 1;
  }
`;

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

export const GoldenPeppaLoading: React.FC = () => {
  return (
    <Box
      data-testid="loading-animation"
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'linear-gradient(135deg, #ffffff 0%, #fafafa 100%)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
      }}
    >
      {/* ロゴアセンブリ */}
      <Box
        sx={{
          position: 'relative',
          width: '300px',
          height: '300px',
          marginBottom: '40px',
        }}
      >
        {/* キラキラエフェクト */}
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '200px',
            height: '200px',
            pointerEvents: 'none',
            zIndex: 15,
          }}
        >
          <Box
            component="img"
            src="/images/キラキラ1.png"
            alt="Sparkle"
            sx={{
              position: 'absolute',
              width: '25px',
              height: '25px',
              objectFit: 'contain',
              opacity: 0,
              animation: `${sparkleFall} 3.2s linear infinite`,
            }}
          />
          <Box
            component="img"
            src="/images/キラキラ2.png"
            alt="Sparkle"
            sx={{
              position: 'absolute',
              width: '25px',
              height: '25px',
              objectFit: 'contain',
              opacity: 0,
              animation: `${sparkleFallRight} 3.2s linear infinite 0.8s`,
            }}
          />
          <Box
            component="img"
            src="/images/キラキラ3.png"
            alt="Sparkle"
            sx={{
              position: 'absolute',
              width: '20px',
              height: '20px',
              objectFit: 'contain',
              opacity: 0,
              animation: `${sparkleFall} 3.2s linear infinite 1.6s`,
            }}
          />
          <Box
            component="img"
            src="/images/キラキラ４.png"
            alt="Sparkle"
            sx={{
              position: 'absolute',
              width: '12.5px',
              height: '12.5px',
              objectFit: 'contain',
              opacity: 0,
              animation: `${sparkleFallRight} 3.2s linear infinite 2.4s`,
            }}
          />
        </Box>

        {/* ペッパーミル */}
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '180px',
            height: '180px',
            zIndex: 10,
          }}
        >
          <Box
            component="img"
            src="/images/peppa.png"
            alt="Golden Peppa"
            sx={{
              width: '100%',
              height: '100%',
              objectFit: 'contain',
              transformOrigin: 'center center',
              animation: `${gentleShake} 4s ease-in-out infinite`,
            }}
          />
          {/* 左下光線 */}
          <Box
            component="img"
            src="/images/左下光線.png"
            alt="Ray"
            sx={{
              position: 'absolute',
              bottom: '10px',
              left: '10px',
              width: '60px',
              height: '80px',
              objectFit: 'contain',
              animation: `${rayGlowPart} 3s ease-in-out infinite`,
            }}
          />
          {/* 右上光線 */}
          <Box
            component="img"
            src="/images/右上光線.png"
            alt="Ray"
            sx={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              width: '60px',
              height: '80px',
              objectFit: 'contain',
              animation: `${rayGlowPart} 3s ease-in-out infinite 0.5s`,
            }}
          />
        </Box>

        {/* ペッパー粒子 */}
        <Box
          sx={{
            position: 'absolute',
            top: 'calc(60% + 30px)',
            left: 'calc(50% + 60px)',
            transform: 'translateX(-50%)',
            width: '60px',
            height: '80px',
            zIndex: 8,
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              left: '30%',
              width: '3px',
              height: '3px',
              background: '#D4AF37',
              borderRadius: '50%',
              opacity: 0,
              boxShadow: '0 0 2px rgba(212, 175, 55, 0.5)',
              animation: `${fallParticle} 2s linear infinite`,
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              left: '50%',
              width: '3px',
              height: '3px',
              background: '#D4AF37',
              borderRadius: '50%',
              opacity: 0,
              boxShadow: '0 0 2px rgba(212, 175, 55, 0.5)',
              animation: `${fallParticle} 2s linear infinite 0.4s`,
            }}
          />
          <Box
            sx={{
              position: 'absolute',
              left: '70%',
              width: '3px',
              height: '3px',
              background: '#D4AF37',
              borderRadius: '50%',
              opacity: 0,
              boxShadow: '0 0 2px rgba(212, 175, 55, 0.5)',
              animation: `${fallParticle} 2s linear infinite 0.8s`,
            }}
          />
        </Box>
      </Box>

      {/* タイトル */}
      <Typography
        variant="h3"
        sx={{
          fontSize: '48px',
          fontWeight: 400,
          color: '#D4AF37',
          marginBottom: '10px',
          letterSpacing: '1px',
          fontFamily: "'Indie Flower', cursive",
          animation: `${fadeInUp} 1s ease-out 0.5s both`,
        }}
      >
        Golden Peppa
      </Typography>

      {/* タグライン */}
      <Typography
        variant="body2"
        sx={{
          fontSize: '14px',
          color: '#666',
          animation: `${fadeInUp} 1s ease-out 0.7s both`,
        }}
      >
        あなたの運命に魔法をかける
      </Typography>

      {/* ローディングドット */}
      <Box
        sx={{
          marginTop: '30px',
          display: 'flex',
          gap: '8px',
          justifyContent: 'center',
          animation: `${fadeIn} 1s ease-out 1s both`,
        }}
      >
        <Box
          sx={{
            width: '8px',
            height: '8px',
            background: '#D4AF37',
            borderRadius: '50%',
            animation: `${dotPulse} 1.5s ease-in-out infinite`,
          }}
        />
        <Box
          sx={{
            width: '8px',
            height: '8px',
            background: '#D4AF37',
            borderRadius: '50%',
            animation: `${dotPulse} 1.5s ease-in-out infinite 0.3s`,
          }}
        />
        <Box
          sx={{
            width: '8px',
            height: '8px',
            background: '#D4AF37',
            borderRadius: '50%',
            animation: `${dotPulse} 1.5s ease-in-out infinite 0.6s`,
          }}
        />
      </Box>
    </Box>
  );
};

export default GoldenPeppaLoading;
