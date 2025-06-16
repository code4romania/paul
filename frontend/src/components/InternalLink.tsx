import { Link } from '@inertiajs/react';
import classNames from 'classnames';

type ExternalLinkProps = {
  color?: string;
  fontSize?: string;
  name: string;
  to: string;
  underline?: boolean;
};

export function InternalLink({
  color = 'text-inherit',
  fontSize,
  name,
  to,
  underline = true,
}: ExternalLinkProps) {
  return (
    <Link className={classNames({ underline }, color, fontSize)} href={to}>
      {name}
    </Link>
  );
}
