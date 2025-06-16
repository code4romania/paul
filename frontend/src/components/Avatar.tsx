import { UserIcon } from '@heroicons/react/20/solid';
import classNames from 'classnames';

type Avatar = {
  size?: 'small' | 'medium' | 'large';
  src?: string;
};

export function Avatar({ size = 'small', src }: Avatar) {
  const styles = classNames(
    'rounded-full bg-gray-100',
    size === 'small' && 'h-8 w-8',
    size === 'medium' && 'h-10 w-10',
    size === 'large' && 'h-16 w-16',
  );
  if (!src) {
    return (
      <div
        className={classNames(
          styles,
          size === 'medium' && 'p-2',
          size === 'large' && 'p-4',
        )}
      >
        <UserIcon className='h-full text-gray-600' />
      </div>
    );
  }

  return <img alt='user avatar' className={styles} src={src} />;
}
