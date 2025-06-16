import classNames from 'classnames';
import { ReactNode } from 'react';

type ExternalLinkProps = {
  color?: string;
  fontSize?: string;
  name: ReactNode;
  to: string;
};

export function ExternalLink({
  color = 'text-inherit',
  fontSize,
  name,
  to,
}: ExternalLinkProps) {
  return (
    <a
      className={classNames('underline break-words', color, fontSize)}
      href={to}
      rel='noreferrer'
      target='_blank'
    >
      {name}
    </a>
  );
}
