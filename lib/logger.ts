/**
 * Centralized Logging Utility
 * Enterprise-grade logging for frontend application
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: any;
}

class Logger {
  private isDevelopment: boolean;
  private isProduction: boolean;

  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
    this.isProduction = process.env.NODE_ENV === 'production';
  }

  private shouldLog(level: LogLevel): boolean {
    // In production, only log warnings and errors
    if (this.isProduction) {
      return level === 'warn' || level === 'error';
    }
    // In development, log everything
    return true;
  }

  private formatMessage(level: LogLevel, message: string, context?: LogContext): string {
    const timestamp = new Date().toISOString();
    const contextStr = context ? ` ${JSON.stringify(context)}` : '';
    return `[${timestamp}] [${level.toUpperCase()}] ${message}${contextStr}`;
  }

  private log(level: LogLevel, message: string, context?: LogContext, error?: Error): void {
    if (!this.shouldLog(level)) {
      return;
    }

    const formattedMessage = this.formatMessage(level, message, context);

    // In production, send to logging service (e.g., Application Insights)
    if (this.isProduction) {
      // TODO: Integrate with Azure Application Insights or other logging service
      // For now, use console but with structured format
      if (level === 'error' && error) {
        console.error(formattedMessage, error);
      } else {
        console[level](formattedMessage);
      }
    } else {
      // In development, use console with full details
      if (level === 'error' && error) {
        console.error(formattedMessage, error);
      } else {
        console[level](formattedMessage);
      }
    }
  }

  debug(message: string, context?: LogContext): void {
    this.log('debug', message, context);
  }

  info(message: string, context?: LogContext): void {
    this.log('info', message, context);
  }

  warn(message: string, context?: LogContext): void {
    this.log('warn', message, context);
  }

  error(message: string, error?: Error, context?: LogContext): void {
    this.log('error', message, context, error);
  }
}

// Export singleton instance
export const logger = new Logger();

// Export for default import
export default logger;

