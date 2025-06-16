import classNames from 'classnames';
import { ButtonHTMLAttributes, MouseEventHandler, ReactNode } from 'react';
import { SvgIcon } from '@/types/SvgIcon';
import { contained, containedError, coreClasses, outlined } from './LinkButton';

type ButtonProps = {
  iconSize?: 'h-4' | 'h-6';
  children?: ReactNode;
  disabled?: boolean;
  endIcon?: SvgIcon;
  fullWidth?: boolean;
  onClick?: MouseEventHandler;
  startIcon?: SvgIcon;
  size?: 'text-lg' | 'text-xs';
  type?: ButtonHTMLAttributes<HTMLButtonElement>['type'];
  variant?: 'contained' | 'outlined' | 'contained-error';
};

export function Button({
  iconSize = 'h-6',
  children,
  disabled,
  endIcon: EndIcon,
  fullWidth,
  onClick,
  startIcon: StartIcon,
  size,
  type,
  variant = 'contained',
}: ButtonProps) {
  return (
    <button
      className={classNames(
        coreClasses,
        disabled && 'bg-gray-200 border text-gray-500',
        variant === 'outlined' && !disabled && outlined,
        variant === 'contained' && !disabled && contained,
        variant === 'contained-error' && containedError,
        size,
        size === 'text-xs' && '!py-1.5 !px-2',
        fullWidth ? 'w-full' : 'w-fit',
      )}
      disabled={disabled}
      onClick={onClick}
      type={type}
    >
      {StartIcon && <StartIcon className={iconSize} />}
      {children}
      {EndIcon && <EndIcon className={iconSize} />}
    </button>
  );
}
