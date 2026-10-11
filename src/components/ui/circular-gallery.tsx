import React, { useState, useEffect, useRef, type HTMLAttributes } from 'react';

export interface GalleryItem {
  name: string;
  description: string;
  href?: string;
  ctaLabel?: string;
  photo: {
    url: string;
    alt: string;
    pos?: string;
  };
}

interface CircularGalleryProps extends HTMLAttributes<HTMLDivElement> {
  items: GalleryItem[];
  radius?: number;
  autoRotateSpeed?: number;
}

// Card dimensions
const CARD_W = 270;
const CARD_H = 390;

const CircularGallery = React.forwardRef<HTMLDivElement, CircularGalleryProps>(
  ({ items, radius = 420, autoRotateSpeed = 0.12, style, ...props }, ref) => {
    const rotRef = useRef(0);
    const [rotation, setRotation] = useState(0);
    const pausedRef = useRef(false);
    const animRef = useRef<number | null>(null);
    const dragRef = useRef({ active: false, startX: 0, startRot: 0 });

    useEffect(() => {
      const tick = () => {
        if (!pausedRef.current) {
          rotRef.current += autoRotateSpeed;
          setRotation(rotRef.current);
        }
        animRef.current = requestAnimationFrame(tick);
      };
      animRef.current = requestAnimationFrame(tick);
      return () => {
        if (animRef.current) cancelAnimationFrame(animRef.current);
      };
    }, [autoRotateSpeed]);

    const onMouseDown = (e: React.MouseEvent) => {
      dragRef.current = { active: true, startX: e.clientX, startRot: rotRef.current };
      pausedRef.current = true;
    };
    const onMouseMove = (e: React.MouseEvent) => {
      if (!dragRef.current.active) return;
      const delta = (dragRef.current.startX - e.clientX) * 0.28;
      rotRef.current = dragRef.current.startRot + delta;
      setRotation(rotRef.current);
    };
    const onMouseUp = () => {
      if (dragRef.current.active) {
        dragRef.current.active = false;
        pausedRef.current = false;
      }
    };

    const onTouchStart = (e: React.TouchEvent) => {
      dragRef.current = { active: true, startX: e.touches[0].clientX, startRot: rotRef.current };
      pausedRef.current = true;
    };
    const onTouchMove = (e: React.TouchEvent) => {
      if (!dragRef.current.active) return;
      const delta = (dragRef.current.startX - e.touches[0].clientX) * 0.28;
      rotRef.current = dragRef.current.startRot + delta;
      setRotation(rotRef.current);
    };
    const onTouchEnd = () => {
      dragRef.current.active = false;
      setTimeout(() => { pausedRef.current = false; }, 800);
    };

    const onCardEnter = () => { if (!dragRef.current.active) pausedRef.current = true; };
    const onCardLeave = () => { if (!dragRef.current.active) pausedRef.current = false; };

    const anglePerItem = 360 / items.length;

    return (
      /* ── Perspective container: fills the wrapper, clipping happens on wrapper ── */
      <div
        ref={ref}
        role="region"
        aria-label="Meteora Experience Gallery"
        {...props}
        style={{
          position: 'relative',
          width: '100%',
          height: '100%',
          perspective: '1800px',
          perspectiveOrigin: '50% 50%',
          userSelect: 'none',
          cursor: dragRef.current.active ? 'grabbing' : 'grab',
          ...style,
        }}
        onMouseDown={onMouseDown}
        onMouseMove={onMouseMove}
        onMouseUp={onMouseUp}
        onMouseLeave={onMouseUp}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        {/*
          ── Rotating hub: zero-size, pinned to exact centre ──
          All cards are children of this element and positioned with
          negative pixel offsets so their visual centre aligns with
          the hub. This guarantees the 3D pivot is always at 50%/50%.
        */}
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            width: 0,
            height: 0,
            transformStyle: 'preserve-3d',
            transform: `rotateY(${rotation}deg)`,
          }}
        >
          {items.map((item, i) => {
            const itemAngle = i * anglePerItem;
            const rel = ((itemAngle + rotation) % 360 + 360) % 360;
            const norm = rel > 180 ? 360 - rel : rel;
            const opacity = Math.max(0.15, 1 - norm / 180);

            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  width: `${CARD_W}px`,
                  height: `${CARD_H}px`,
                  /* Centre the card on the hub */
                  left: `${-CARD_W / 2}px`,
                  top: `${-CARD_H / 2}px`,
                  transform: `rotateY(${itemAngle}deg) translateZ(${radius}px)`,
                  opacity,
                  transition: 'opacity 0.25s linear',
                }}
                onMouseEnter={onCardEnter}
                onMouseLeave={onCardLeave}
              >
                <div
                  style={{
                    position: 'relative',
                    width: '100%',
                    height: '100%',
                    borderRadius: '4px',
                    overflow: 'hidden',
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(10,7,5,0.7)',
                  }}
                >
                  <img
                    src={item.photo.url}
                    alt={item.photo.alt}
                    draggable={false}
                    style={{
                      position: 'absolute',
                      inset: 0,
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                      objectPosition: item.photo.pos ?? 'center',
                      pointerEvents: 'none',
                    }}
                  />
                  <div
                    style={{
                      position: 'absolute',
                      bottom: 0,
                      left: 0,
                      width: '100%',
                      padding: '2rem 1rem 1rem',
                      background:
                        'linear-gradient(to top, rgba(5,3,2,0.96) 0%, rgba(5,3,2,0.55) 55%, transparent 100%)',
                    }}
                  >
                    <h3
                      style={{
                        fontFamily:
                          '"Cormorant Garamond Variable", "Cormorant Garamond", Georgia, serif',
                        fontSize: '1.4rem',
                        fontWeight: 300,
                        lineHeight: 1.2,
                        color: '#fff',
                        margin: '0 0 0.3rem',
                      }}
                    >
                      {item.name}
                    </h3>
                    <p
                      style={{
                        fontFamily: '"Jost Variable", Jost, sans-serif',
                        fontSize: '0.68rem',
                        color: 'rgba(255,255,255,0.62)',
                        margin: '0 0 0.75rem',
                        letterSpacing: '0.03em',
                        lineHeight: 1.4,
                      }}
                    >
                      {item.description}
                    </p>
                    {item.href && (
                      <a
                        href={item.href}
                        draggable={false}
                        style={{
                          display: 'inline-block',
                          padding: '0.3rem 0.85rem',
                          border: '1px solid rgba(184,158,114,0.65)',
                          borderRadius: '2px',
                          color: 'rgb(184,158,114)',
                          fontFamily: '"Jost Variable", Jost, sans-serif',
                          fontSize: '0.58rem',
                          fontWeight: 500,
                          letterSpacing: '0.12em',
                          textTransform: 'uppercase',
                          textDecoration: 'none',
                        }}
                        onMouseDown={e => e.stopPropagation()}
                      >
                        {item.ctaLabel ?? 'Scopri'}
                      </a>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
);

CircularGallery.displayName = 'CircularGallery';

export { CircularGallery };
