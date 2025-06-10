import { Link } from '@inertiajs/react';
import classnames from 'classnames';
import { KeyboardEvent, MouseEvent, ReactNode } from 'react';
import { SvgIcon } from '@/types/SvgIcon';

export const contained = 'bg-primary-main';
export const containedError = 'bg-red-100 text-error hover:bg-rose-200';
export const outlined = 'border border-gray-300 text-gray-700 bg-white';
const white = 'bg-white text-black';

export const coreClasses =
  'flex items-center font-amalia-medium px-4 py-2.5 rounded-md text-black justify-center gap-x-2 text-sm whitespace-nowrap shadow hover:shadow-md';

type PrimaryButtonProps = {
  children: ReactNode;
  endIcon?: SvgIcon;
  fullWidth?: boolean;
  iconSize?: 'h-4' | 'h-6';
  onClick?: (
    event: MouseEvent<Element> | KeyboardEvent<Element>,
  ) => void;
  to: string;
  variant?: 'contained' | 'outlined' | 'white' | 'contained-error';
  size?: string;
};

export function LinkButton({
  children,
  endIcon: EndIcon,
  fullWidth,
  iconSize = 'h-6',
  onClick,
  to,
  variant = 'outlined',
  size,
}: PrimaryButtonProps) {
  return (
    <Link
      className={classnames(
        coreClasses,
        variant === 'contained' && contained,
        variant === 'contained-error' && containedError,
        variant === 'outlined' && outlined,
        variant === 'white' && white,
        size,
        fullWidth ? 'w-full' : 'w-fit',
      )}
      href={to}
      onClick={onClick}
    >
      {children}

      {EndIcon && <EndIcon className={iconSize} />}
    </Link>
  );
}
