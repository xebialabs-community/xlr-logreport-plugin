# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import org.slf4j.LoggerFactory;


import ch.qos.logback.classic.Logger as Logger
import ch.qos.logback.classic.LoggerContext as LoggerContext
import ch.qos.logback.classic.encoder.PatternLayoutEncoder as PatternLayoutEncoder
import ch.qos.logback.classic.sift.MDCBasedDiscriminator as MDCBasedDiscriminator
import ch.qos.logback.classic.sift.SiftingAppender as SiftingAppender
import ch.qos.logback.classic.spi.ILoggingEvent as ILoggingEvent
import ch.qos.logback.core.Appender as Appender
import ch.qos.logback.core.Context as Context
import ch.qos.logback.core.joran.spi.JoranException as JoranException
import ch.qos.logback.core.rolling.RollingFileAppender as RollingFileAppender
import ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP as SizeAndTimeBasedFNATP
import ch.qos.logback.core.rolling.TimeBasedRollingPolicy as TimeBasedRollingPolicy
import ch.qos.logback.core.sift.AppenderFactory as AppenderFactory

def buildAppender( context, discriminatingValue):
    ple = PatternLayoutEncoder()
    ple.setPattern("%date [%thread] [%file:%line] %msg%n")
    ple.setContext(context)
    ple.start()
    logFileAppender = new RollingFileAppender();
    logFileAppender.setContext(context);
    logFileAppender.setName("File-"+discriminatingValue);
    logFileAppender.setEncoder(ple);
    logFileAppender.setFile(filename+"-"+discriminatingValue+".txt");

    SizeAndTimeBasedRollingPolicy<ILoggingEvent> logFilePolicy = new SizeAndTimeBasedRollingPolicy();
    logFilePolicy.setContext(context);
    logFilePolicy.setParent(logFileAppender);
    logFilePolicy.setFileNamePattern(filename+"-"+discriminatingValue+".log");
    logFilePolicy.setMaxHistory(5);
    logFilePolicy.setMaxFileSize(FileSize.valueOf("512kb"));
    logFilePolicy.setTotalSizeCap(FileSize.valueOf("1gb"));
    logFilePolicy.start();

    logFileAppender.setRollingPolicy(logFilePolicy);
    logFileAppender.start();

    logFileAppender.start();
    return logFileAppender;


def putNewAppender(file, log):
    lc = LoggerFactory.getILoggerFactory()
    logger = lc.getLogger(log.getName())
    SiftingAppender sa = SiftingAppender()
    sa.setName("SIFT")
    sa.setContext(lc)

    discriminator = MDCBasedDiscriminator()
    discriminator.setKey("logFileName")
    discriminator.setDefaultValue("head0")
    discriminator.start()

    sa.setDiscriminator(discriminator)

    sa.setAppenderFactory(buildAppender(lc, discriminator))
    sa.start();
    logger.addAppender(sa);
    logger.setAdditive(false);

    return logger;


def tail(f, n, offset=None):
    """Reads a n lines from f with an offset of offset lines.  The return
    value is a tuple in the form ``(lines, has_more)`` where `has_more` is
    an indicator that is `True` if there are more lines in the file.
    """
    avg_line_length = 74
    to_read = n + (offset or 0)

    while 1:
        try:
            fo = open(f, "r+")
            fo.seek(-(avg_line_length * to_read), 2)
        except IOError:
            # woops.  apparently file is smaller than what we want
            # to step back, go to the beginning instead
            fo.seek(0)
        pos = fo.tell()
        lines = fo.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            fo.close()
            return lines[-to_read:offset and -offset or None], \
                   len(lines) > to_read or pos > 0
        avg_line_length *= 1.3

if __name__ == "__main__":
   filename = "container.log"
   tail(filename,10)
response.entity = {"status": "OK"}
